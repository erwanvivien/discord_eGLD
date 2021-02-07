import discord
import os
from discord.ext import commands


# import discord_utils
import utils
import database as db

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


db.create()
client = Client()
client.run(token)
