import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

import numpy as np

import datetime
import database as db


years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
days = mdates.DayLocator()  # every month
years_fmt = mdates.DateFormatter('%Y')


def create_graph(lastdays=1):
    start = datetime.datetime.now()
    sql = "SELECT * FROM prices WHERE date >= ? ORDER BY date DESC LIMIT ?"
    args = (datetime.datetime.strftime(
        datetime.datetime.now() - datetime.timedelta(days=lastdays),
        r"%Y-%m-%d %H"), lastdays * 1440)
    rows = db.exec(sql, args)

    print(datetime.datetime.now() - datetime.timedelta(days=lastdays))
    print("query:\t", datetime.datetime.now() - start)

    start = datetime.datetime.now()
    dates = []
    values = []
    for row in rows:
        row_date = datetime.datetime.strptime(
            row[db.PRICES_DATE], r"%Y-%m-%d %H:%M:%S.%f")
        if datetime.datetime.now() - datetime.timedelta(days=lastdays) <= row_date:
            dates.append(row_date)
            values.append(row[db.PRICES_VAL])

    print("filter:\t", datetime.datetime.now() - start)

    start = datetime.datetime.now()
    fig, ax = plt.subplots()

    ax.plot(dates, values)

    ymax = max(values)
    xpos = values.index(ymax)
    xmax = dates[xpos]

    ymin = min(values)
    xpos = values.index(ymin)
    xmin = dates[xpos]

    ax.annotate(f"max: {ymax}", xy=(xmax, ymax), xytext=(xmax, ymax + 0.1))
    ax.annotate(f"min: {ymin}", xy=(xmin, ymin), xytext=(xmin, ymin - 0.1))

    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    print("graph:\t", datetime.datetime.now() - start)

    start = datetime.datetime.now()
    plt.plot()
    plt.savefig(f'graph_{lastdays}.png')
    print("plot:\t", datetime.datetime.now() - start)
    print()
