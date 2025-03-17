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

correlation_id = "stream _1"
action = 1
mode = 1
token_list = [{"exchangeType": 1, "tokens": ["99926000"]}]

sws = SmartWebSocketV2(data["data"]["jwtToken"], key_secret[0], key_secret[2], feed_token)



def on_data(wsapp, message):
    print("Ticks: {}".format(message))
    
def on_open(wsapp):
    logger.info("on open")
    sws.subscribe(correlation_id, mode, token_list)
    # sws.unsubscribe(correlation_id, mode, token_list1)

def on_error(wsapp, error):
    logger.error(error)
    
def on_close(wsapp):
    logger.info("Close")

    
sws.on_open = on_open
sws.on_data = on_data
sws.on_error = on_error
sws.on_close = on_close


sws.connect()

# def place_limit_order(ticker,buy_sell, price, quantity):
#             params = {
#         "variety":"NORMAL",
#         "tradingsymbol":"{}-EQ".format(ticker),
#         "symboltoken":token_lookup(ticker, instrument_list),
#         "transactiontype":buy_sell,
#         "exchange":"NSE",
#         "ordertype":"LIMIT",
#         "producttype":"INTRADAY",
#         "duration":"DAY",
#         "price":price,
#         "quantity":quantity
#         }
#             response = obj.placeOrder(params)
#             return response
    
# order_id = place_limit_order("RELIANCE", "BUY", 1230, 1)
# print(order_id)


# def cancel_order(order_id, variety):
#     response = obj.cancelOrder(order_id, variety)
#     return response

# cancel_order = cancel_order(order_id, "NORMAL")

# def get_open_erders():
#     response = obj.orderBook()
#     return response

# open_orders = get_open_erders()
