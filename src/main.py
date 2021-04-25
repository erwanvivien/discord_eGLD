import discord
import os
from discord.ext import commands
import asyncio
import datetime


import discord_utils as disc
import database as db
import utils
import binance

ERRORS = []

DISC_LNK = "https://discord.com/api/oauth2/authorize?client_id=807967570962939914&permissions=10304&scope=bot"

token = utils.get_content("token")

last_log_file = datetime.datetime.now()
last_update_egld = datetime.datetime.now() - datetime.timedelta(minutes=60)


CMDS = {
    # Link to a wallet
    "egld$set": utils.add,
    "egld$join": utils.add,
    "egld$link": utils.add,

    # Unlink a wallet
    "egld$unset": utils.delete,
    "egld$delete": utils.delete,
    "egld$unlink": utils.delete,

    # Display
    "egld$value": utils.value,
    "egld$stat": utils.stats,
    "egld$stats": utils.stats,
    "egld$graph": utils.graph,
    "egld$wallet": utils.display_me,

    # Server display
    "egld$stonks": utils.display,
    "egld$wallets": utils.display,

    # Link / Unlink all wallets accross all servers
    "me$delete": utils.delete_all,
    "me$remove": utils.delete_all,

    # Help message
    "egld$help": utils.help,

    # Display how many servers are running
    "egld$server": utils.servers,
    "egld$servers": utils.servers,
    "egld$guild": utils.servers,
    "egld$guilds": utils.servers,

    # Display how many members are using the bot
    "egld$member": utils.members,
    "egld$members": utils.members,

    # Send report messages
    "egld$report": utils.report,

    # Dev commands
    "egld$dev$prices": utils.dev_prices,
    "egld$dev$clean": utils.dev_clean,
    "egld$dev$clear": utils.dev_clean,
    "egld$dev$create": utils.dev_create,
}


class Client(discord.Client):
    async def on_ready(self):
        print(f'[eGLD] Logged on as {self.user}')
        print(f"invite link: ↓\n{DISC_LNK}")
        print('==============================================================================================')
        print()

        # await client.change_presence(
        #     status=discord.Status.online,
        #     activity=discord.Activity(
        #         name="eGLD !",
        #         type=discord.ActivityType.watching))

        await disc.report(self, "Started", "Started successfully !")

    async def on_message(self, message):
        if message.author.id in utils.BOT_IDS:        # Doesn't do anything if it's a bot message
            return

        split = message.content.split(' ', 1)  # separate mom?[cmd] from args
        cmd = split[0].lower()
        args = split[1].split(' ') if len(split) > 1 else []

        # Get Discord Nick if existant or discord Name
        name = disc.author_name(message.author, False)

        # Runs command if it's a known command
        if cmd in CMDS:
            utils.check_member(message)
            utils.log("on_message", "Command execution",
                      f"{name} from discord {message.guild.id} issued {cmd} command. <{args}>")

            await CMDS[cmd](self, message, args)


db.create()
client = Client()


async def cron():
    global last_log_file
    global last_update_egld

    sql = "SELECT val FROM prices ORDER BY val DESC LIMIT 1"
    max_price = db.exec(sql)[0][0]

    sql = "SELECT val FROM prices ORDER BY val ASC LIMIT 1"
    min_price = db.exec(sql)[0][0]

    # ALWAYS CLEAR LOG FILE HERE
    await client.wait_until_ready()

    while True:
        try:
            # Resets the log file every two days
            if last_log_file + datetime.timedelta(days=2) < datetime.datetime.now():
                f = open(utils.LOG_FILE, "w")
                f.close()
                last_log_file = datetime.datetime.now()
                utils.log("cron", "Reseted the log file", "RESET!!")

            # Updates the price
            binance.update()

            # Appends to the DB every 2 mins' results & if it's a new high / low
            if binance.price >= 0 and (last_update_egld + datetime.timedelta(minutes=2) < datetime.datetime.now()
                                       or binance.price < min_price or binance.price > max_price):
                sql = "INSERT INTO prices (val, date) VALUES (?, ?)"
                sql_args = [binance.price, str(datetime.datetime.now())]

                db.exec(sql, sql_args)

                last_update_egld = datetime.datetime.now()

                if binance.price < min_price:
                    min_price = binance.price
                if binance.price > max_price:
                    max_price = binance.price

            # Updated the bot's status
            await client.change_presence(
                status=discord.Status.online,
                activity=discord.Activity(
                    name=f"eGLD: {binance.price}$",
                    type=discord.ActivityType.watching))

            await asyncio.sleep(15)
        except Exception as e:
            print(e)
            print(type(e))
            await disc.report(client, "Error in CRON loop\nWaiting 1 minute.", str(e))

client.loop.create_task(cron())
client.run(token)
