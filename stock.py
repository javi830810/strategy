from datetime import datetime
from datetime import date

class Stock:
    
    def __init__(self, daily_data=[]):
        def create_indexes():
            index = 0
            
            daily_index = {}
            month_index = {}
            year_index = {}
            
            year_start = None
            year_end = None
            month_start = None
            month_end = None
            last_year = None
            last_month = None

            previous_day = None
            for day in daily_data:
                daily_index["%s_%s_%s" % (day.year(), day.month(), day.day())] = day

                if last_year != day.year():
                    year_start = index
                year_end = index

                if last_month != day.month():
                    month_start = index
                month_end = index
                
                last_year = day.year()
                last_month = day.month()

                year_index[day.year()] = (year_start, year_end)
                month_index["%s_%s " %(day.year(),day.month())] = (month_start, month_end)

                if previous_day:
                    previous_day.next_day = day
                day.previous_day = previous_day
                previous_day = day

                index += 1

            return daily_index, month_index, year_index

        self.daily_data = daily_data
        self.daily_index, self.month_index, self.year_index = create_indexes()

    def year_min(self, year):
        result = None
        for day in self._year(year):
            if not result or day.close() < result.close():
                result = day
        return result

    def month_min(self, year, month):
        result = None
        for day in self._month(year, month):
            if not result or day.close() < result.close():
                result = day
        return result

    def ma_50(self, date=None):
        return self._ma_x(50, date)

    def ma_200(self, date=None):
        return self._ma_x(200, date)    

    def fifty_two_weeks_high(self, date=None):
        return self._high_x(365, date)

    #Private Methods
    def _ma_x(self, amout_of_days, date=None):
        if date and isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d')
        elif not date:
            date = date.today()
        
        daily = self.price_near_at(date)

        avg = 0
        i = 0
        while i < amout_of_days:
            avg += daily.close()
            daily = daily.previous_day
            i += 1
        
        return avg/amout_of_days

    def _high_x(self, amout_of_days, date=None):
        if date and isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d')
        elif not date:
            date = date.today()
        
        daily = self.price_near_at(date)

        max_day = 0
        i = 0
        while i < amout_of_days:
            max_day = max(daily.close(), max_day)
            daily = daily.previous_day
            i += 1
        
        return max_day

    def price_near_at(self, date):
        month_daily = self._month(date.year, date.month)
        closest_day = None
        for day in month_daily:
            if not closest_day:
                closest_day = day
            elif abs(closest_day.day() - date.day) > abs(day.day() - date.day):
                closest_day = day
                
        return closest_day

    def price_at(self, date):
        return self.daily_index.get("%s_%s_%s" % (date.year, date.month, date.day), None)
    
    def _month(self, year, month):
        month_tuple = self.month_index.get("%s_%s " %(year,month))
        return self.daily_data[month_tuple[0]:month_tuple[1]]

    def _year(self, year):
        year_tuple = self.year_index.get(year)
        return self.daily_data[year_tuple[0]:year_tuple[1]]    

class MonthlyStock:
    def __init__(self, year, month, daily_data=[]):
        self._year = year
        self._month = month
        self.daily_data = daily_data

    def month(self):
        return self._month

    def year(self):
        return self._year

class DailyStock:

    def __init__(self, date, close):
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.close_value = float(close)
        self.next_day = None
        self.previous_day = None

    def month(self):
        return self.date.month

    def day(self):
        return self.date.day

    def year(self):
        return self.date.year

    def close(self):
        return self.close_value


def read_data(symbol):
    file1 = open("data/%s.csv" % symbol, 'r') 
    lines = file1.readlines() 
    
    daily_data = []
    
    last_month = None

    for line in lines[1:]:         
        try:
            data = line.split(",")
            daily_data.append(DailyStock(data[0], data[5]))
        except ValueError:
            # print(line)
            # print("Oops!  That was no valid number.  moving on...")
            continue

    return Stock(daily_data)
    

def min_monthly(symbol):
    pass

def days_to_invest(symbol, min_monthly_data):
    pass

def run(symbol, start_date):
    pass


# appl_stock = read_data('AAPL')
# test_date = date(2017, 3, 15)
# print("Min Value in Year %s: %s " % (test_date.year, appl_stock.year_min(test_date.year).close()))
# print("Min Value in Month/Year %s/%s: %s " % (test_date.month, test_date.year, appl_stock.month_min(test_date.year, test_date.month).close()))
# print("50 day moving Average in %s: %s " % (test_date, appl_stock.ma_50(test_date)))
# print("200 day moving Average in %s: %s " % (test_date, appl_stock.ma_200(test_date)))
# print("52 Weeks High in %s: %s " % (test_date, appl_stock.fifty_two_weeks_high(test_date)))

# print("\n")

# test_date = date(2020, 3, 15)
# print("Min Value in Year %s: %s " % (test_date.year, appl_stock.year_min(test_date.year).close()))
# print("Min Value in Month/Year %s/%s: %s " % (test_date.month, test_date.year, appl_stock.month_min(test_date.year, test_date.month).close()))
# print("50 day moving Average in %s: %s " % (test_date, appl_stock.ma_50(test_date)))
# print("200 day moving Average in %s: %s " % (test_date, appl_stock.ma_200(test_date)))
# print("52 Weeks High in %s: %s " % (test_date, appl_stock.fifty_two_weeks_high(test_date)))
