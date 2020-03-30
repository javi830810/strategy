from datetime import datetime
from datetime import date 
from dateutil.relativedelta import relativedelta
from stock import read_data

class EveryDay15:

    def should_execute(self, date):
        return False
    
    def amount(self, date):
        return 0

    def run(self, stock, start_date, end_date=None, initial_amount=0, increase_monthly=0):
        current_amount = initial_amount
        total_shares = 0
        current_date = start_date    
        total_cost = 0
        total_amount = initial_amount

        current_date = date(start_date.year, start_date.month, 15)

        while current_date < end_date:
            month_expenses = 0
            month_shares = 0

            total_amount += increase_monthly    
            current_amount += increase_monthly
            price_today = stock.price_near_at(current_date)

            month_shares = current_amount // price_today.close()
            month_expenses = price_today.close() * month_shares

            print("Buying at: %s, Amount: %s, Cost: %s" %(current_date, month_shares, month_expenses))
            current_date = current_date + relativedelta(months=1)

            total_cost += month_expenses
            total_shares += month_shares
            current_amount -= month_expenses        

        return {
                    "shares": total_shares,
                    "cash": current_amount,
                    "cost": total_cost,
                    "avg_price_share": total_cost/total_shares
        }    

                    
    def _first_day_of_next_month(self, _date):
        return date(_date.year, _date.month, 1) + relativedelta(months=1)

    def _last_day_of_month(self, _date):
        return date(_date.year, _date.month, 1) + relativedelta(months=1, days=-1)

    def _previous_month(self, _date):
        return _date - relativedelta(months=1)


strategy1 = EveryDay15()
appl_stock = read_data('SPY')
start_date = date(2018, 1, 1)
end_date = date(2020, 3, 10)

result = strategy1.run(appl_stock, start_date, end_date, 0, 1000)

print("\n")
print(result)
print("Cost: %s" % result["cost"])
print("Value: %s" %(result["shares"] * appl_stock.price_near_at(end_date).close()))
