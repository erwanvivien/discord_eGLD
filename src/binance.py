import requests


def get_price(name):
    r = requests.get(
        f"https://api.binance.com/api/v3/ticker/price?symbol={name}")
    js = r.json()

    if not "price" in js:
        return -1

    return round(float(js["price"]), 2)


def stats(name):
    r = requests.get(
        f"https://api.binance.com/api/v3/ticker/24hr?symbol={name}")
    js = r.json()

    if not "priceChange" in js:
        return (-100000, -100000)

    return (round(float(js["priceChange"]), 2), round(float(js["priceChangePercent"]), 2))
