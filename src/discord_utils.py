import discord
import random
# from utils import subreddit_json, get_content
import database as db
import utils

WRONG_USAGE = "Something went wrong"
HELP_USAGE = "Please see `egld$help` for further information"
HOWTO_URL = "https://github.com/erwanvivien/discord-egold"
ICON_URL = "https://raw.githubusercontent.com/erwanvivien/discord-eGLD/main/imgs/goldr-icon.png"

BOT_COLOR = discord.Colour(0xFBDC1B)
ERROR_COLOR = discord.Colour(0xff0000)
WARN_COLOR = discord.Colour(0xebdb34)
VALID_COLOR = discord.Colour(0x55da50)


def author_name(author, discriminator=True):
    # Get nick from msg author (discord) if exists
    if not discriminator:
        return author.display_name
    return f"{author.name}#{author.discriminator}"


def create_embed(title, desc, colour=BOT_COLOR, url=HOWTO_URL, icon_url="", footer_url=ICON_URL, footer_text="Goldr"):
    embed = discord.Embed(title=title,
                          description=desc,
                          colour=colour,
                          url=url)

    if icon_url:
        embed.set_thumbnail(url=icon_url)
    if footer_url or footer_text:
        embed.set_footer(text=footer_text, icon_url=footer_url)

    return embed


async def error_message(message, title=WRONG_USAGE, desc=HELP_USAGE, url=HOWTO_URL,
                        icon_url="", footer_url=ICON_URL, footer_text="Goldr"):
    # Sends error message to discord (red)
    return await message.channel.send(embed=create_embed(title, desc, ERROR_COLOR, url, icon_url, footer_url, footer_text))


async def send_message(message, title=WRONG_USAGE, desc=HELP_USAGE, url=HOWTO_URL,
                       icon_url="", footer_url=ICON_URL, footer_text="Goldr"):
    # Sends message to discord (bot_color)
    return await message.channel.send(embed=create_embed(title, desc, BOT_COLOR, url, icon_url, footer_url, footer_text))


async def send_file(message, filename, content=""):
    # Sends message to discord (bot_color)
    return await message.channel.send(content, file=discord.File(filename))


async def edit_message(message, title=WRONG_USAGE, desc=HELP_USAGE, url=HOWTO_URL,
                       icon_url="", footer_url=ICON_URL, footer_text="Goldr"):
    # Sends message to discord (bot_color)
    return await message.edit(embed=create_embed(title, desc, BOT_COLOR, url, icon_url, footer_url, footer_text))
