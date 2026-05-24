#api key - DA37EKM855YLSFT9
# finnhub key - d88ehb9r01qq4342rhe0d88ehb9r01qq4342rheg
# api for getting name - https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo

import requests
import time
from utils import check_input_float, check_input_num, call_get_api, safe_get
from dataclasses import dataclass

NAME_URL = "https://finnhub.io/api/v1/stock/profile2"
QUOTE_URL = "https://finnhub.io/api/v1/quote"
API_KEY = "d88ehb9r01qq4342rhe0d88ehb9r01qq4342rheg"

@dataclass
class Stock:
    symbol: str
    name: str
    current: float
    day_high: float
    day_low: float
    open_price: float
    previous_close: float
    change: float
    change_percent: float


def call_api(list_symbols):
    #print("Symbol : ", symbol)
    stocks = []
    for symbol in list_symbols :
        symbol = symbol.strip()
        params = {
            "symbol": symbol,
            "token": API_KEY
        }
        res = call_get_api(NAME_URL, params)
        if (res is None) or not (isinstance(res, dict)):
            print(f"{symbol} -> No response")
            continue
        if "name" not in res:
            print(f"{symbol} -> Stock not found")
            continue
        name = res["name"]
        res = call_get_api(QUOTE_URL, params)
        if (res is None) or not (isinstance(res, dict)):
            print(f"{symbol} -> No response")
            continue
        open_price = safe_get(res, "o", 0.0)
        day_high = safe_get(res, "h", 0.0)
        day_low = safe_get(res, "l", 0.0)
        current = safe_get(res, "c", 0.0)
        previous_close = safe_get(res, "pc", 0.0)
        change = safe_get(res, "d", 0.0)
        change_percent = safe_get(res, "dp", 0.0)
        stk = Stock(
            symbol=symbol,
            name=name,
            open_price=open_price,
            day_high=day_high,
            day_low=day_low,
            current=current,
            previous_close=previous_close,
            change=change,
            change_percent=change_percent
        )
        stocks.append(stk)
    return stocks

def print_stock(stock) :
    #print(stock)
    text = "============================================================\n"
    text = text + f" {stock.symbol} - {stock.name}\n"
    text = text + "============================================================\n"
    text = text + f"Current Price     : {stock.current}\n"
    text = text + f"Open              : {stock.open_price}\n"
    text = text + f"Previous Close    : {stock.previous_close}\n"
    text = text + f"Day Range         : {stock.day_low} - {stock.day_high}\n"
    text = text + "Change            : "
    if stock.change > 0 :
        text = text + f"+{stock.change} (+{stock.change_percent}%)"
    else :
        text = text + f"{stock.change} ({stock.change_percent}%)"
    text = text + "\n============================================================\n"
    return text

def get_input():
    symbol = input("Enter ticker symbol(s) : ")
    return symbol.upper()
    
if __name__ == "__main__":
    symbol = get_input()
    list_symbols = symbol.split(",")
    #print(list_symbols)    
    stocks = call_api(list_symbols)
    #print(stocks)
    for stk in stocks :
        print(print_stock(stk))

