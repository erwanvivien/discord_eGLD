import sqlite3
from sqlite3 import Error
import os

import utils


DB_PATH = "db/database.db"


def create():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.close()

    sql_create_members = """CREATE TABLE IF NOT EXISTS members
    (
        id              INTEGER NOT NULL PRIMARY KEY,
        id_discord      INTEGER NOT NULL,

        wallet          TEXT,

        FOREIGN KEY(id_discord) REFERENCES discords(id)
    );"""
    exec(sql_create_members)


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


def member_exist(member_id, guild_id=None):
    sql = f'''SELECT * FROM members WHERE id = {member_id}'''
    db = exec(sql)

    for row in db:
        if member_id == row[0]:
            return True

    return False


def member_add(member_id, guild_id):
    sql = f'''INSERT INTO members (id, id_discord, wallet) VALUES (?, ?, ?)'''
    args = [member_id, guild_id, ""]
    exec(sql, args)


def member_delete(member_id, guild_id=None):
    sql = f'''DELETE FROM members WHERE id = {member_id}'''
    exec(sql)


if not os.path.exists("db"):
    utils.log("DB folder", "DB folder did not exist", "Creating DB folder")

    os.mkdir("db")
    f = open(utils.LOG_FILE, "w")
    f.close()
