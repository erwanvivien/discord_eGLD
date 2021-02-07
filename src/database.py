import sqlite3
from sqlite3 import Error
import os

import utils


DB_PATH = "db/database.db"

POS_ID = 0
POS_NAME = 1
POS_GUILD = 2
POS_WALLET = 3


def create():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.close()

    sql_create_members = """CREATE TABLE IF NOT EXISTS members
    (
        id              INTEGER NOT NULL,
        name            TEXT NOT NULL,
        id_discord      INTEGER NOT NULL,

        wallet          TEXT
    );"""
    exec(sql_create_members)


def exec(sql, sql_args=None):
    conn = sqlite3.connect(DB_PATH)
    if not conn:
        return None
    cur = conn.cursor()

    if sql_args:
        res = cur.execute(sql, sql_args).fetchall()
    else:
        res = cur.execute(sql).fetchall()

    conn.commit()
    conn.close()

    return res


def member_exist(message):
    sql = f'''SELECT * FROM members WHERE id = ? AND id_discord = ?'''
    sql_args = [message.author.id, message.guild.id]
    db = exec(sql, sql_args)

    for row in db:
        if message.author.id == row[0]:
            return True

    return False


def member_add(message):
    sql = f'''INSERT INTO members (id, name, id_discord, wallet) VALUES (?, ?, ?, ?)'''
    sql_args = [message.author.id,
                message.author.name, message.guild.id, ""]
    exec(sql, sql_args)


def member_delete(message):
    sql = f'''DELETE FROM members WHERE id = ? AND id_discord = ?'''
    sql_args = [message.author.id, message.guild.id]
    exec(sql, sql_args)


if not os.path.exists("db"):
    utils.log("DB folder", "DB folder did not exist", "Creating DB folder")

    os.mkdir("db")
    f = open(utils.LOG_FILE, "w")
    f.close()
