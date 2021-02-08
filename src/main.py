import discord
import os
from discord.ext import commands
import asyncio
import datetime


import discord_utils
import database as db
import utils
import binance

BOT_IDS = []
DEV_IDS = [289145021922279425]

ERRORS = []

DISC_LNK = "https://discord.com/api/oauth2/authorize?client_id=807967570962939914&permissions=10304&scope=bot"

token = utils.get_content("token_dev")

last_log_file = datetime.datetime.now()


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
    "egld$wallet": utils.display_me,

    # Server display
    "egld$wallets": utils.display,

    # Link / Unlink all wallets accross all servers
    "me$delete": utils.delete_all,
    "me$remove": utils.delete_all,

    # Help message
    "egld$help": utils.help,

    "egld$server": utils.servers,
    "egld$servers": utils.servers,
    "egld$guild": utils.servers,
    "egld$guilds": utils.servers,

    "egld$member": utils.members,
    "egld$members": utils.members,
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

    async def on_message(self, message):
        if message.author.id in BOT_IDS:        # Doesn't do anything if it's a bot message
            return

        split = message.content.split(' ', 1)  # separate mom?[cmd] from args
        cmd = split[0].lower()
        args = split[1].split(' ') if len(split) > 1 else []

        # Get Discord Nick if existant or discord Name
        name = discord_utils.author_name(message.author, False)

        # Runs command if it's a known command
        if cmd in CMDS:
            utils.check_member(message)
            utils.log("on_message", "Command execution",
                      f"{name} from discord {message.guild.id} issued {cmd} command. <{args}>")

            await CMDS[cmd](self, message, args)


db.create()
client = Client()


async def status_task():
    await client.wait_until_ready()
    while True:
        if last_log_file + datetime.timedelta(days=2) < datetime.datetime.now():
            f = open(utils.LOG_FILE, "w")  # resets the file
            f.close()

        binance.update()

        await client.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                name=f"eGLD: {binance.price}$",
                type=discord.ActivityType.watching))

        await asyncio.sleep(15)

client.loop.create_task(status_task())
client.run(token)
