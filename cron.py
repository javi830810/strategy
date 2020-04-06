from datetime import datetime
from datetime import date

import requests
from common import download_symbol, read_data
import minimum_month_strategy
from pymongo import MongoClient
from config import mongo_host, mongo_port
from stock import DailyStock, Stock

def job(database, symbol):
    today = date.today() # today

    # Update to Today First
    print("Updating Data for Symbol %s" %symbol)
    download_symbol(stocks_collection, symbol)

    print("Analizing Data for Symbol %s" %symbol)
    stock = read_data(stocks_collection, symbol)

    strategy = minimum_month_strategy.Strategy()
    st = strategy.buy_at(stock, today)
    
    results = {}
    results["_date"] = today
    results.update(st)
    print(results)
    r = requests.post("https://maker.ifttt.com/trigger/buyspy/with/key/lgZ2-PIbeA4ZzkBFem8M-u933GuzypBiSCim4JUesVH", data = {"value1": str(results["price_today"]), "value2": str(results["minimun_last_month"]), "value3": "Buy" if results["buy"] else "DO NOT BUY"})
    print(r.content)


mongo_client = MongoClient(mongo_host, mongo_port)
db = mongo_client["strategy"]
stocks_collection = db["stocks"]
job(stocks_collection, "SPY")