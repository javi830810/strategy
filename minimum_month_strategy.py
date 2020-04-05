from datetime import datetime
from datetime import date 
from dateutil.relativedelta import relativedelta

class Strategy:

    def should_execute(self, date):
        return False
    
    def amount(self, date):
        return 0

    def buy_at(self, stock, current_date=date.today()):

        prev_month = self._previous_month(date.today())
        min_prev_month = stock.month_min(prev_month.year, prev_month.month) if stock.has_data_for_month(prev_month.year, prev_month.month) else None
        # if current_date == date.today():
        #     price_today = stock.price_at(current_date)
        # else:
        price_today = stock.price_now()
        
        return {
                "price_today": round(price_today,2) if price_today else "NO_DATA",
                "minimun_last_month": round(min_prev_month.close(),2) if min_prev_month else "NO_DATA",
                "buy": price_today < min_prev_month.close() if min_prev_month and price_today else False,
                "stock": stock.symbol
            }

    def run(self, stock, start_date, end_date=None, initial_amount=0, increase_monthly=0, verbose=False):
        current_amount = initial_amount
        total_shares = 0
        current_date = start_date    
        total_cost = 0
        total_amount = initial_amount

        while current_date < end_date:
            month_expenses = 0
            month_shares = 0

            total_amount += increase_monthly    
            current_amount += increase_monthly
            current_month = current_date
            
            while current_date <= self._last_day_of_month(current_month) and current_date <= end_date:
                
                prev_month = self._previous_month(current_date)
                min_prev_month = stock.month_min(prev_month.year, prev_month.month)
                price_today = stock.price_at(current_date)

                if price_today and price_today.close() < min_prev_month.close():
                    month_shares = current_amount // price_today.close()
                    month_expenses = price_today.close() * month_shares
                    
                    if verbose:
                        print("Buying at: %s, Amount: %s, Cost: %s" %(current_date, month_shares, month_expenses))

                    current_date = self._first_day_of_next_month(current_date)
                    break
                current_date = current_date + relativedelta(days=1)

            total_cost += month_expenses
            total_shares += month_shares
            current_amount -= month_expenses        


        value = total_shares*stock.price_near_at(end_date).close()
        cost = round(total_cost,2)

        return {
                    "name": "Buy when Lower than Minimum last month",
                    "shares": round(total_shares,2),
                    "cash": round(current_amount,2),
                    "cost": cost,
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