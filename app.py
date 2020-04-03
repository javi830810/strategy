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
from common import download_symbol, read_data

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

mongo_client = MongoClient(mongo_host, mongo_port)



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