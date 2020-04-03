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