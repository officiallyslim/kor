import discord
from discord.ext import commands
import requests
import pytz
from discord.ext import tasks, commands
import random
from datetime import datetime
import asyncio
import dotenv
import os

bot = discord.Bot()
intents = discord.Intents.all()
intents.message_content = True
intents.messages = True
intents.guild_messages = True
bot = commands.Bot(command_prefix="a!", intents=intents)

admins = [756509638169460837]

# Links
island_base_url = "https://robloxislands.fandom.com"
embed_url = "http://144.76.143.198:8165/getEmbed"
fact_list_github = "https://github.com/Stageddat/kor/blob/main/src/facts/island_fact/facts_list.md"

# Github token
dotenv.load_dotenv()
github_token = str(os.getenv("GITHUB_TOKEN"))