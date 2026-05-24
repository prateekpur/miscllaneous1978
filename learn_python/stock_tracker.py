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


def call_api(symbol):
    #print("Symbol : ", symbol)
    params = {
        "symbol": symbol,
        "token": API_KEY
    }
    res = call_get_api(NAME_URL, params)
    if (res is None) or not (isinstance(res, dict)):
        print("No response")
        return
    if "name" not in res:
        print("Stock not found")
        return
    name = res["name"]
    res = call_get_api(QUOTE_URL, params)
    if (res is None) or not (isinstance(res, dict)):
        print("No response")
        return
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
    return stk

def get_input():
    symbol = input("Enter ticker symbol : ")
    return symbol.upper()
    
if __name__ == "__main__":
    symbol = get_input()
    print(call_api(symbol))

