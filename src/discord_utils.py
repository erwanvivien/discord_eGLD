import discord
import random
# from utils import subreddit_json, get_content
import database as db
import utils

WRONG_USAGE = "Something went wrong"
HELP_USAGE = "Please see `egld$help` for further information"
HOWTO_URL = "https://github.com/erwanvivien/discord-egold"

BOT_COLOR = discord.Colour(0x8b8349)
ERROR_COLOR = discord.Colour(0xff0000)
WARN_COLOR = discord.Colour(0xebdb34)
VALID_COLOR = discord.Colour(0x55da50)


def author_name(author, discriminator=True):
    # Get nick from msg author (discord) if exists
    if not discriminator:
        return author.display_name
    return f"{author.name}#{author.discriminator}"


def create_embed(title, desc, colour=BOT_COLOR, url=HOWTO_URL):
    return discord.Embed(title=title,
                         description=desc,
                         colour=colour,
                         url=url)


async def error_message(message, title=WRONG_USAGE, desc=HELP_USAGE, url=HOWTO_URL):
    # Sends error message to discord (red)
    try:
        return await message.channel.send(embed=create_embed(title, desc, ERROR_COLOR, url))
    except Exception as error:
        utils.log("error_message", error,
                  "Could not send **error** message to discord")


async def send_message(message, title=WRONG_USAGE, desc=HELP_USAGE, url=HOWTO_URL):
    # Sends message to discord (bot_color)
    try:
        return await message.channel.send(embed=create_embed(title, desc, BOT_COLOR, url))
    except Exception as error:
        utils.log("error_message", error,
                  "Could not send message to discord")


async def edit_message(message, title=WRONG_USAGE, desc=HELP_USAGE, url=HOWTO_URL):
    # Sends message to discord (bot_color)
    try:
        return await message.edit(embed=create_embed(title, desc, BOT_COLOR, url))
    except Exception as error:
        utils.log("error_message", error,
                  "Could not edit message")
