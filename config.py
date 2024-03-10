import discord
from discord.ext import commands
import requests
import pytz
from discord.ext import tasks, commands
import random
from datetime import datetime
import asyncio

bot = discord.Bot()
intents = discord.Intents.all()
intents.message_content = True
intents.messages = True
intents.guild_messages = True
bot = commands.Bot(command_prefix="a!", intents=intents)

admins = [756509638169460837]

# CHANNELS
fact_channel_id_debug = 1216056844506759278

junior_role = 1155823367623020586
moderator_role = 843816627018530838
admin_role = 1150091304831823912