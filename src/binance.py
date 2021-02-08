import requests
import datetime

import utils


price = -1
priceChange = -1
priceChangePercent = -1
last_update = datetime.datetime.now() - datetime.timedelta(minutes=10)


def update_price():
    global last_update
    if last_update + datetime.timedelta(seconds=50) >= datetime.datetime.now():
        utils.log("update_price", "PRICE has NOT been update",
                  f"last_update: {last_update} & now: {datetime.datetime.now()}")
        return

    r = requests.get(
        f"https://api.binance.com/api/v3/ticker/price?symbol=EGLDUSDT")
    js = r.json()

    if not "price" in js:
        utils.log("update_stats", "PRICESTATS has NOT been update",
                  f"Could not fetch stats from binance")
        return

    global price
    price = round(float(js["price"]), 2)
    utils.log("update_price", "PRICE has been update",
              f"New price is {price}$ !")
    last_update = datetime.datetime.now()


def update_stats():
    global last_update
    if last_update + datetime.timedelta(seconds=50) >= datetime.datetime.now():
        utils.log("update_stats", "PRICESTATS has NOT been update",
                  f"last_update: {last_update} & now: {datetime.datetime.now()}")
        return

    r = requests.get(
        f"https://api.binance.com/api/v3/ticker/24hr?symbol=EGLDUSDT")
    js = r.json()

    if not "priceChange" in js:
        utils.log("update_stats", "PRICESTATS has NOT been update",
                  f"Could not fetch stats from binance")
        return

    global priceChange
    global priceChangePercent

    (priceChange, priceChangePercent) = (
        round(float(js["priceChange"]), 2), round(float(js["priceChangePercent"]), 2))
    utils.log("update_stats", "PRICESTATS has been update",
              f"New price is {priceChange}$ & {priceChangePercent}% !")


def update():
    update_stats()
    update_price()


def get_price(name):
    r = requests.get(
        f"https://api.binance.com/api/v3/ticker/price?symbol={name}")
    js = r.json()

    if not "price" in js:
        return -1

    price = round(float(js["price"]), 2)
    return price
