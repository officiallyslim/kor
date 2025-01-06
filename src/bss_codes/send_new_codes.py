import json
from src.global_src.global_path import bssUpdateCodesPath
from config import bot

def loadUpdateCodesData():
    try:
        with open(bssUpdateCodesPath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

async def sendNewCodeNotification(code):
    updateCodes = loadUpdateCodesData()
    channel = await bot.fetch_channel(updateCodes["notificationChannelID"])
    await channel.send(f"New code: {code}")