from SmartApi.smartConnect import SmartConnect
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from pyotp import TOTP
from logzero import logger
import os
import urllib
import json
import pandas as pd
import datetime as dt
import time


TOTP("C24DAETDNWHMVQ4S5B2JHS4H2Q").now()

key_path = "/Users/vikask/Downloads/Python/Angel_one_api"
os.chdir(key_path)


with open("angel_keys.txt", "r") as file:
    key_secret = file.read().split()
    
obj = SmartConnect(api_key = key_secret[0])

data = obj.generateSession(key_secret[2], key_secret[3], TOTP(key_secret[4]).now())
feed_token = obj.getfeedToken()

instrument_url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
response = urllib.request.urlopen(instrument_url)

instrument_list = json.loads(response.read())
print(f"instrument_list fetch successful")

tickers = ["INFY", "ITC", "RELIANCE"]

def token_lookup(ticker, instrument_list, exchange = "NSE"):
    for instrument in instrument_list:
        if instrument["name"] == ticker and instrument["exch_seg"] == exchange and instrument["symbol"].split("-")[-1] == "EQ":
            return instrument["token"]


def symbol_lookup(token, instrument_list, exchange = "NSE"):
    for instrument in instrument_list:
        if instrument["token"] == token:
            return instrument["name"]


def hist_data(tickers, duration, interval, instrument_list, exchange = "NSE"):
    # global df_data
    hist_data_tickers = {}
    for ticker in tickers:
        params = {
             "exchange": exchange,
             "symboltoken": token_lookup(ticker, instrument_list),
             "interval": interval,
             "fromdate": (dt.date.today() - dt.timedelta(duration)).strftime("%Y-%m-%d %H:%M"),
             "todate": dt.date.today().strftime("%Y-%m-%d %H:%M")
        }
        hist_data = obj.getCandleData(params)
        df_data = pd.DataFrame(hist_data["data"], columns = ["date", "open", "high", "low", "close", "volume"])
        df_data.set_index("date", inplace = True)
        df_data.index = pd.to_datetime(df_data.index)
        df_data.index = df_data.index.tz_localize(None)
        hist_data_tickers[ticker] = df_data
    return hist_data_tickers


candle_Data = hist_data(tickers, 90, "ONE_DAY", instrument_list)

