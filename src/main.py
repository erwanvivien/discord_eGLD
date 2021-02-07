import discord
import os
from discord.ext import commands


import discord_utils
import database as db
import utils

BOT_IDS = []
DEV_IDS = [289145021922279425]

ERRORS = []

DISC_LNK = "https://discord.com/api/oauth2/authorize?client_id=807967570962939914&permissions=10304&scope=bot"

token = utils.get_content("token_dev")


CMDS = {
    "egld$add": utils.add,
    "egld$wallet": utils.add,
    "egld$link": utils.add,

    "egld$delete": utils.delete,
    "egld$remove": utils.delete,
    "egld$unlink": utils.delete,
}


class Client(discord.Client):
    async def on_ready(self):
        print(f'[eGLD] Logged on as {self.user}')
        print(f"invite link: ↓\n{DISC_LNK}")
        print('==============================================================================================')
        print()

        try:
            await client.change_presence(
                status=discord.Status.online,
                activity=discord.Activity(
                    name="eGLD !",
                    type=discord.ActivityType.watching))
        except Exception as error:
            utils.log("on_ready", error,
                      "Couldn't change bot's presence")

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
client.run(token)
