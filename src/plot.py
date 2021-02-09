import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

import datetime
import database as db


years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
days = mdates.DayLocator()  # every month
years_fmt = mdates.DateFormatter('%Y')


def create_graph(period="day"):
    sql = "SELECT * FROM prices ORDER BY date DESC LIMIT 500"
    rows = db.exec(sql)

    dates = [datetime.datetime.strptime(
        row[db.PRICES_DATE], "%Y-%m-%d %H:%M:%S.%f") for row in rows]

    values = [row[db.PRICES_VAL] for row in rows]

    fig, ax = plt.subplots()
    ax.plot(dates, values)

    ax.xaxis.set_major_locator(days)
    ax.set_xlim(dates[-1], dates[0])

    ymin = min(values)
    xpos = values.index(ymin)
    xmin = values[xpos]

    ymax = max(values)
    xpos = values.index(ymax)
    xmax = values[xpos]

    ax.set_ylim(xmin - 0.5, xmax + 0.5)

    ax.annotate(f"max: {ymax}", xy=(xmax, ymax), xytext=(xmax, ymax+5))

    fig.autofmt_xdate()

    plt.plot()
    plt.savefig(f'graph_{period}.png')
