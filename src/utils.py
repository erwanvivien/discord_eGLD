import requests
import json

import os
import datetime

import database as db
import discord_utils as disc

import binance

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
    if not db.member_exist(message):
        log("check_member", "Adding member",
            f"Added member {message.author.id} with guild {message.guild.id}")
        db.member_add(message)


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

    await disc.send_message(message, title="💹 Success !", desc=f"{disc.author_name(message.author)} successfully linked his eGLD wallet")


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
    if len(args) == 0:
        price = binance.price
        return await disc.send_message(message, title="Current value eGLD",
                                       desc=f"Current price is **{price}**",
                                       url="https://www.binance.com/en-NG/trade/EGLD_BTC")

    currency = args[0]
    currency_check = currency.replace("_", "")
    price = binance.get_price(currency_check)
    if price < 0:
        return await disc.error_message(message, title=f"😱 Oops... !",
                                        desc=f"We could not fetch any information about {currency}" +
                                        f"See if the money exists here: https://www.binance.com/en-NG/trade/{currency}")

    return await disc.send_message(message, title=f"Current value {currency}",
                                   desc=f"Current price is **{price}**",
                                   url=f"https://www.binance.com/en-NG/trade/{currency}")


def get_account_tokens(wallet):
    r = requests.get(f"https://api.elrond.com/address/{wallet}")
    js = r.json()
    if "error" in js:
        return js["error"]

    balance = float(js["data"]["account"]["balance"])
    tokens = balance / 1000000000000000000

    return str(tokens)


def pretty_string(name, egld, usdt):
    s_egld = str(egld)
    s_usdt = str(usdt)

    s = f"{name}"
    s += ' ' * (25 - len(s) - len(s_egld))
    s += f"{egld}"
    s += ' ' * (38 - len(s) - len(s_usdt))
    s += f"{usdt}\n"
    # s += ' ' * (60 - len(s))
    return s


async def display_me(self, message, args):
    sql = f"SELECT * FROM members WHERE id = ? AND id_discord = ?"
    sql_args = [message.author.id, message.guild.id]
    res = db.exec(sql, sql_args)

    if not res or not res[0][db.POS_WALLET]:
        return await disc.error_message(message, title="🤯 Oops...",
                                        desc="You probably just forgot to link your wallet !\nSee `egold$help` for more informations")

    wallet = res[0][db.POS_WALLET]
    tokens = round(float(get_account_tokens(wallet)), 4)
    price = binance.price
    equi = tokens * price

    try:
        tokens = float(tokens)
        await disc.send_message(message, title="Current balance",
                                desc=f"You currently have **{tokens} eGLD** which convert to **{equi}$**",
                                url="https://wallet.elrond.com/")
    except:
        await disc.error_message(message, title="Something went wrong !",
                                 desc="We got an error from Elrond when checking your wallet\nError is `" + tokens + "`")


async def display(self, message, args):
    sql = f"SELECT * FROM members WHERE id_discord = ?"
    sql_args = [message.guild.id]
    res = db.exec(sql, sql_args)

    price = binance.price
    all = pretty_string("NAME", "EGLD", "USD") + "\n"
    all += pretty_string("Current", "1", price)
    all += ('-' * 38) + '\n'

    total_egld = 0
    total_usdt = 0

    for member in res:
        if not member or not member[db.POS_WALLET]:
            continue  # Treat this as empty

        tokens = round(float(get_account_tokens(member[db.POS_WALLET])), 4)
        equi = round(tokens * price, 2)
        total_egld += tokens
        total_usdt += equi
        all += pretty_string(member[1], tokens, equi)

    all += ('=' * 38) + '\n'
    all += pretty_string("Total:", total_egld, round(total_usdt, 2))

    emj1 = "↗" if binance.priceChange > 0 else "↘"
    emj2 = "↗" if binance.priceChangePercent > 0 else "↘"

    s = f"{emj1} {binance.priceChange}$ ----- EGLD ----- {emj2} {binance.priceChangePercent}% last 24H"

    await disc.send_message(message, title=s,
                            desc=f"```\n{all}\n```",
                            url="https://wallet.elrond.com/")


async def help(self, message, args):
    help_str = get_content("help")
    await disc.send_message(message, title="Help !", desc=help_str)


async def stats(self, message, args):
    emj1 = "↗" if binance.priceChange > 0 else "↘"
    emj2 = "↗" if binance.priceChangePercent > 0 else "↘"

    s = f"{emj1} {binance.priceChange}$\n{emj2} {binance.priceChangePercent}%"
    return await disc.send_message(message, title="Last's 24h", desc=s)


async def servers(self, message, args):
    sql = "SELECT DISTINCT(id_discord) FROM members"
    sql_answer = db.exec(sql)

    count = len(sql_answer)
    await disc.send_message(message, title="Number of servers connected",
                            desc=f"Currently there are `{count}` servers using the bot.",
                            url="")


async def members(self, message, args):
    sql = "SELECT DISTINCT(id) FROM members"
    sql_answer = db.exec(sql)

    count = len(sql_answer)
    await disc.send_message(message, title="Number of members connected",
                            desc=f"Currently there are `{count}` members using the bot.",
                            url="")

if not os.path.exists("db"):
    os.mkdir("db")
    f = open(LOG_FILE, "w")
    f.close()

    # After because we need the folder
    log("DB folder", "DB folder did not exist", "Creating DB folder")
