import sqlite3
from sqlite3 import Error
import os

import utils


DB_PATH = "db/database.db"


def create():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.close()

    # sql_create_discord = """CREATE TABLE IF NOT EXISTS discords
    # (
    #     id INTEGER NOT NULL PRIMARY KEY
    # );
    # """
    # exec(sql_create_discord)


def exec(sql, args=None):
    conn = sqlite3.connect(DB_PATH)
    if not conn:
        return None
    cur = conn.cursor()

    if args:
        res = cur.execute(sql, args).fetchall()
    else:
        res = cur.execute(sql).fetchall()

    conn.commit()
    conn.close()

    return res


if not os.path.exists("db"):
    utils.log("DB folder", "DB folder did not exist", "Creating DB folder")

    os.mkdir("db")
    f = open(utils.LOG_FILE, "w")
    f.close()
