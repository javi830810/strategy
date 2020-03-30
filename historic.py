import symbols
import requests

def download_symbol(symbol):
    url = "https://query1.finance.yahoo.com/v7/finance/download/%s?period1=953942400&period2=1585094400&interval=1d&events=history" % symbol
    r = requests.get(url, allow_redirects=False)
    open("data/%s.csv" %symbol, 'wb').write(r.content)
    
for symbol in symbols.all:
    print("Downloading Data for Symbol: %s" % symbol )
    download_symbol(symbol)

