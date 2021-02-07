import requests
import json

import os
import datetime

import database as db
import discord_utils as disc


LOG_FILE = "db/log"


def get_content(file):
    # Read file content
    try:
        file = open(file, "r")
        s = file.read()
        file.close()
    except Exception as error:
        log("get_content", error, f"error reading file {file}")
        return ""

    return s


def log(fctname, error, message):
    """
    Pretty printer for logs
    """

    now = datetime.datetime.now()
    log = f"[{now}]: " + \
        str(error) + '\n' + ('+' * 4) + (' ' * 4) + \
        fctname + (" " * (20-len(fctname))) + \
        ': ' + message + '\n'

    print(log)

    f = open(LOG_FILE, "a+")

    f.write(log)
    f.close()


def check_member(message):
    if not db.member_exist(message.author.id, message.guild.id):
        log("check_member", "Adding member",
            f"Added member {message.author.id} with guild {message.guild.id}")
        db.member_add(message.author.id, message.guild.id)


def check_token(address):
    r = requests.get(f"https://api.elrond.com/address/{address}")
    js = r.json()

    if "error" in js:
        log("check_token", "Bad address",
            f"Address {address} is not fetchable.")
        return f"error {r.status_code}: " + js["error"]
    return ""


async def add(self, message, args):
    await message.delete()
    if len(args) != 1:
        return await disc.error_message(message, title="🤯 Wrong usage",
                                        desc="The `add` function takes only `1` parameter, the Maiar wallet ID")

    address = args[0]
    error_code = check_token(address)
    if error_code != "":
        return await disc.error_message(message, title="⁉ Wrong address",
                                        desc="You did not provide a good address\n" +
                                        f"eGLD sent this: `{error_code}`")

    sql = """UPDATE members SET wallet = ? WHERE id = ? AND id_discord = ?"""
    sql_args = [args[0], message.author.id, message.guild.id]
    db.exec(sql, sql_args)

    await disc.send_message(message, title="💹 Success !", desc="You successfully linked your eGLD wallet")


async def delete(self, message, args):
    sql = """UPDATE members SET wallet = ? WHERE id = ? AND id_discord = ?"""
    sql_args = ["", message.author.id, message.guild.id]
    db.exec(sql, sql_args)


async def add_all(self, message, args):
    sql = """UPDATE members SET wallet = ? WHERE id = ?"""
    sql_args = ["", message.author.id]
    db.exec(sql, sql_args)


async def delete_all(self, message, args):
    sql = """UPDATE members SET wallet = ? WHERE id = ?"""
    sql_args = ["", message.author.id]
    db.exec(sql, sql_args)


async def delete_member(self, message, args):
    sql = """DELETE FROM members WHERE id = ?"""
    sql_args = [message.author.id]
    db.exec(sql, sql_args)


async def value(self, message, args):
    pass


async def display_me(self, message, args):
    sql = f"SELECT * FROM members WHERE id = ? AND id_discord = ?"
    sql_args = [message.author.id, message.guild.id]
    res = db.exec(sql, sql_args)

    if not res:
        return await disc.error_message(message, title="🤯 Oops...",
                                        desc="You probably just forgot to link your wallet !\nSee `egold$help` for more informations")
    wallet = res[0][2]  # 3rd value is the wallet
    r = requests.get(f"https://api.elrond.com/address/{wallet}")
    js = r.json()
    if "error" in js:
        return await disc.error_message(message, title="Something went wrong !",
                                        desc="We got an error from Elrond when checking your wallet\nError is `" + js["error"] + "`")

    balance = float(js["data"]["account"]["balance"])
    tokens = balance / 1000000000000000000
    await disc.send_message(message, title="Current balance",
                            desc=f"You currently have **{tokens} eGLD** which convert to ...",
                            url="https://wallet.elrond.com/")


async def display(self, message, args):
    pass


if not os.path.exists("db"):
    os.mkdir("db")
    f = open(LOG_FILE, "w")
    f.close()

    # After because we need the folder
    log("DB folder", "DB folder did not exist", "Creating DB folder")
