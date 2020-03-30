
from datetime import datetime
from datetime import date 
import minimum_month_strategy
import buy_lower_50_ma_strategy
import buy_lower_200_ma_strategy
import every_day_15_strategy
from stock import read_data

start_date = date(2015, 1, 1)
end_date = date(2020, 3, 20)
appl_stock = read_data('SPY')

results = {}

strategy = buy_lower_50_ma_strategy.Strategy()
st = strategy.run(appl_stock, start_date, end_date, 0, 1000)
results[st["name"]] = st

strategy = buy_lower_200_ma_strategy.Strategy()
st = strategy.run(appl_stock, start_date, end_date, 0, 1000)
results[st["name"]] = st

strategy = minimum_month_strategy.Strategy()
st = strategy.run(appl_stock, start_date, end_date, 0, 1000)
results[st["name"]] = st

strategy = every_day_15_strategy.Strategy()
st = strategy.run(appl_stock, start_date, end_date, 0, 1000)
results[st["name"]] = st

results["start_date"] = start_date
results["end_date"] = end_date
print(results)