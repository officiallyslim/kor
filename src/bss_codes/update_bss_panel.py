import json
from config import bot
from src.global_src.global_path import bss_codes_path, bssUpdateCodesPath
from src.bss_codes.scrap_wiki import scrap_wiki
import discord
from datetime import datetime
from src.bss_codes.send_new_codes import sendNewCodeNotification
from src.bss_codes.show_more import showMoreView

def loadCodes():
    try:
        with open(bss_codes_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def loadUpdateCodesData():
    try:
        with open(bssUpdateCodesPath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


async def updateBssCodes():
    try:
        newsCodes, invalidCodes, commonCodes = await scrap_wiki()
    except Exception as e:
        print(e)
        return "Failed"
    updateCodes = loadUpdateCodesData()
    try:
        channel = await bot.fetch_channel(updateCodes["panelChannelID"])
        try:
            message = await channel.fetch_message(updateCodes["panelMessageID"])
        except Exception as e:
            print(f"Failed fetch bss code msg panel {e}")
            message = await channel.send("Starting...")

            # save new msg id
            updateCodes["panelMessageID"] = message.id
            with open(bssUpdateCodesPath, "w") as file:
                json.dump(updateCodes, file, indent=4)
        if message:
            embed = await refactCodes(updateCodes["updateFrequency"])
            await message.edit(content="", embed=embed, view=showMoreView())
    except Exception as e:
        print(e)
        return "Failed"

    if newsCodes is not None:
        for code in newsCodes:
            await sendNewCodeNotification(code)

    return newsCodes, invalidCodes, commonCodes


async def refactCodes(time):
    codes = loadCodes()

    codesList = ""
    for code in codes:
        codesList += f"- {code}\n"

    codesEmbed = discord.Embed(
        title="BSS Working Codes",
        description=f"{codesList}\n\nUpdated <t:{int(datetime.now().timestamp())}:R>\nNext update <t:{int(datetime.now().timestamp()) + time}:R>",
        colour=discord.Colour(int("6798ed", 16)),
    )

    return codesEmbed
