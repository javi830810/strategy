from flask import Flask
from flask import jsonify
from flask import request

from datetime import datetime
from datetime import date 
import minimum_month_strategy
from pymongo import MongoClient

import symbols
import requests
import csv

import uuid 

import minimum_month_strategy
from stock import DailyStock, Stock
from config import mongo_host, mongo_port

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

mongo_client = MongoClient(mongo_host, mongo_port)

def download_symbol(database, symbol):
    start_date = 953942400 #03/25/2000
    end_date = int(datetime.utcnow().timestamp()) # today

    url = "https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=1d&events=history" % (symbol,start_date, end_date)

    r = requests.get(url, allow_redirects=False)
    decoded_content = r.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    index = 0

    # Delete all records of the symbol in DB
    database.delete_many({"symbol": symbol})

    for row in cr:
        if not index:
            index = 1
            continue
        try:
            record_date = datetime.strptime(row[0], '%Y-%m-%d')
            stock_record = {
                'symbol': symbol,
                'date': record_date,
                'open': row[1],
                'high': row[2],
                'close': row[3],
                'adj_close': row[4],
                'volume': row[5]
            }
            
            database.insert_one(stock_record)

        except ValueError:
            print(row)
            # print("Oops!  That was no valid number.  moving on...")
            continue

def read_data(stocks_collection, symbol):
    def skiplimit(collection, page_size=50, page_num=0):
        """returns a set of documents belonging to page number `page_num`
        where size of each page is `page_size`.
        """

        # Skip and limit
        cursor = collection.find({"symbol": symbol}).sort("date").skip(page_num*page_size).limit(page_size)
        return [DailyStock(x["date"], x["close"]) for x in cursor]

    daily_data = []
    page_num = 0
    data = skiplimit(stocks_collection, 200, page_num)
    
    while data:
        daily_data += data
        page_num += 1
        data = skiplimit(stocks_collection, 200, page_num)
    
    return Stock(symbol, daily_data)

@app.route('/symbols/<symbol>/strategy/minimum_month')
def minimum_month_strat(symbol):
    start_date = date.fromisoformat(request.args.get('start'))
    end_date = date.fromisoformat(request.args.get('end'))

    db = mongo_client["strategy"]
    stocks_collection = db["stocks"]
    stock = read_data(stocks_collection, symbol)

    strategy = minimum_month_strategy.Strategy()
    st = strategy.run(stock, start_date, end_date, 0, 1000)
    
    results = {}
    results["_start_date"] = start_date
    results["_end_date"] = end_date
    results.update(st)

    return jsonify(results)

@app.route('/symbols/<symbol>/strategy/minimum_month/should_buy')
def should_buy(symbol):
    at_date = date.fromisoformat(request.args.get('date'))

    db = mongo_client["strategy"]
    stocks_collection = db["stocks"]
    stock = read_data(stocks_collection, symbol)

    strategy = minimum_month_strategy.Strategy()
    st = strategy.buy_at(stock, at_date)
    
    results = {}
    results["_date"] = at_date
    results.update(st)

    return jsonify(results)

@app.route('/symbols/<symbol>', methods = ['POST'])
def pull_symbol(symbol):
    db = mongo_client["strategy"]
    stocks_collection = db["stocks"]
    download_symbol(stocks_collection, symbol)
    return jsonify(symbol)

@app.route('/symbols/<symbol>', methods = ['GET'])
def get_symbol(symbol):
    """Return a friendly HTTP greeting."""
    return jsonify(symbol)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')