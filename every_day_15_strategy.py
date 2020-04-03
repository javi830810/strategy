from datetime import datetime
from datetime import date 
from dateutil.relativedelta import relativedelta
from stock import read_data

class Strategy:

    def should_execute(self, date):
        return False
    
    def amount(self, date):
        return 0

    def run(self, stock, start_date, end_date=None, initial_amount=0, increase_monthly=0, verbose=False):
        current_amount = initial_amount
        total_shares = 0
        current_date = start_date    
        total_cost = 0
        total_amount = initial_amount

        current_date = date(start_date.year, start_date.month, 20)

        while current_date < end_date:
            month_expenses = 0
            month_shares = 0

            total_amount += increase_monthly    
            current_amount += increase_monthly
            price_today = stock.price_near_at(current_date)

            month_shares = current_amount // price_today.close()
            month_expenses = price_today.close() * month_shares

            if verbose:
                print("Buying at: %s, Amount: %s, Cost: %s" %(current_date, month_shares, month_expenses))
            current_date = current_date + relativedelta(months=1)

            total_cost += month_expenses
            total_shares += month_shares
            current_amount -= month_expenses        

        value = total_shares*stock.price_near_at(end_date).close()
        cost = round(total_cost,2)
        
        return {
                    "name": "Buy Every day 15",
                    "shares": round(total_shares,2),
                    "cash": round(current_amount,2),
                    "cost": round(total_cost,2),
                    "profit": round(value - total_cost,2),
                    "profit(%)": round( (value - total_cost) *100/cost ,2),
                    "avg_price_share": round(total_cost/total_shares,2)
        }    

                    
    def _first_day_of_next_month(self, _date):
        return date(_date.year, _date.month, 1) + relativedelta(months=1)

    def _last_day_of_month(self, _date):
        return date(_date.year, _date.month, 1) + relativedelta(months=1, days=-1)

    def _previous_month(self, _date):
        return _date - relativedelta(months=1)
