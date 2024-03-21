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

# CHANNELS
fact_channel_id_debug = 1216056844506759278
daily_fact_log_channel_id = 1217895141902123111
general_log_channel_id = 1217894520658722866
new_members_log_channel_id = 1220141824979505193

welcome_channel_id = 1220135931659554908
# Path
facts_md_path = 'src/facts/island_fact/facts_list.md'
daily_count_path = 'src/facts/daily_count.txt'
added_trivia_path = 'src/facts/island_fact/added_trivia.json'
island_fact_database_path = 'src/facts/island_fact/island_fact.json'
new_fact_path = 'src/facts/new_fact.txt'
error_fact_path = 'src/facts/error_fact/error_fact.json'

embed_path = 'src/embed_sender/embed.json'

default_pfp_path = 'src/new_member/new_member_img/defaultpfp.png'
pfp_img_path = 'src/new_member/new_member_img/user_pfp.png'
background_img_path = 'src/new_member/new_member_img/background.png'
welcome_img_folder_path = 'src/new_member/old_welcome_img/'

# Staff Roles
mr_boomsteak = 1210006813945106492
developer = 1214469615808417812
head_of_operations = 1168385225349406771
assistant_director = 1151613202669514813
community_manager = 1175981569656225862
staff_manager = 1175986076125515786
head_administration = 1216518080889622538
senior_administration = 1216518078649860198
official_administration = 1216518079433936975
junior_administration = 1175985559743774791
trial_administration = 1175985971565694987
mr_boomsteaks_controller = 1151613201377677382
management_team = 1175984805620494426
head_of_moderation = 1216518081032093766
senior_moderator = 1175982839481782353
official_moderator = 1151613205089628212
junior_moderator = 1216506577251733615
trial_moderator = 1151613206939324578

# Links
island_base_url = "https://robloxislands.fandom.com"
embed_url = "http://144.76.143.198:8165/getEmbed"
fact_list_github = "https://github.com/Stageddat/kor/blob/main/src/facts/island_fact/facts_list.md"

# Github raw links
dotenv.load_dotenv()
github_token = str(os.getenv("GITHUB_TOKEN"))

raw_fact_list_github = f"https://raw.githubusercontent.com/Stageddat/kor/main/src/facts/island_fact/facts_list.md"
raw_fact_database_github = f"https://raw.githubusercontent.com/Stageddat/kor/main/src/facts/island_fact/island_fact.json"
raw_added_fact_github = f"https://raw.githubusercontent.com/Stageddat/kor/main/src/factsisland_fact//added_trivia.json"

# Img links
