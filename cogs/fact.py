from config import *
from discord.commands import Option
from commands.fact_commands import fact_group
from src.global_embeds import no_perm_embed, soon_embed, error_embed, failed_fetch_daily_channel
from src.facts.island_fact import check_existing_link, check_link, extract_trivia, push_facts_github
import json
import os
import dotenv

async def send_facts_as_file(ctx: discord.ApplicationContext, facts):
    facts_str = '\n'.join(facts) if isinstance(facts, list) else str(facts)

    with open(new_fact_path, 'w', encoding='utf-8') as file:
        file.write(facts_str)

    with open(new_fact_path, 'rb') as file:
        await ctx.respond(f"Added the following facts. **PLEASE CHECK IF THERE ARE ANY ERRORS**. Click the below button if u need help.\nIf you want see the whole log, visit [Github]({fact_list_github})", file=discord.File(file, 'facts.txt'), ephemeral=True, view=error_trivia_help())

class error_trivia_help(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Help", style=discord.ButtonStyle.primary, emoji="➕", custom_id="fact_error_help")
    async def fact_error_help(self, button: discord.ui.Button, interaction: discord.Interaction):
        with open(error_fact_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        help_embed = [discord.Embed.from_dict(embed_info) for embed_info in data[0]['embeds']] if data[0]['embeds'] else None

        await interaction.response.send_message(embeds=help_embed, ephemeral=True)

class fact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name = "change_fact_number", description = "Change the daily fact number")
    async def change_fact_number(self, ctx: discord.ApplicationContext, number: Option(int, "The next say fact number")): # type: ignore
        if int(ctx.author.id) != 756509638169460837 and not any(role.id in [
                staff_manager,
                community_manager,
                assistant_director,
                head_of_operations,
                developer,
                mr_boomsteak] for role in ctx.author.roles):
            await ctx.respond(embed=no_perm_embed, ephemeral=True)
            return

        if not float(number).is_integer():
            await ctx.respond("Please enter an integer without decimals!", ephemeral=True)
            return

        f = open(daily_count_path, "w")
        f.write(f"{number}")
        f.close()

        await ctx.respond(f"The next daily count number set to `{number}`", ephemeral=True)

        daily_log_channel = bot.get_channel(daily_fact_log_channel_id)
        general_kor_log_channel = bot.get_channel(general_log_channel_id)

        if daily_log_channel:
            embed = discord.Embed(
                title="Updated daily count",
                description=f"{ctx.author.mention} (`{ctx.author.id}`) updated the daily count to `{number}`",
                colour=discord.Colour(int("51d1f6", 16))
            )
            await daily_log_channel.send(embed=embed)
        else:
            await general_kor_log_channel.send(embed=failed_fetch_daily_channel)

    @discord.slash_command(name = "add_custom_island_fact", description = "Add new island fact to database")
    async def add_custom_island_fact(self, ctx: discord.ApplicationContext, fact: Option(str, "Fact about Islands (Roblox)"), img_link: Option(str, "Related image of the fact") = None, source_link: Option(str, "Source link of the fact") = None):# type: ignore
        if int(ctx.author.id) != 756509638169460837 and not any(role.id in [
                staff_manager,
                community_manager,
                assistant_director,
                head_of_operations,
                developer,
                mr_boomsteak] for role in ctx.author.roles):
            await ctx.respond(embed=no_perm_embed, ephemeral=True)
            return

        await ctx.respond(embed=soon_embed, ephemeral=True)

    @discord.slash_command(name = "add_island_trivia", description = "Add fact of trivia from official Island Wiki")
    async def add_island_trivia(self, ctx: discord.ApplicationContext, link: Option(str, "Island Wiki link")):# type: ignore
        await ctx.defer(ephemeral=True)
        if int(ctx.author.id) != 756509638169460837 and not any(role.id in [
                staff_manager,
                community_manager,
                assistant_director,
                head_of_operations,
                developer,
                mr_boomsteak] for role in ctx.author.roles):
            await ctx.respond(embed=no_perm_embed, ephemeral=True)
            return
        
        if await check_link(link):
            if not await check_existing_link(link):
                facts = await extract_trivia(link, ctx.user.name)
                if facts == "No trivia":
                    await ctx.respond(f"No trivia found!", ephemeral=True)
                else:
                    await send_facts_as_file(ctx, facts)

            else:
                existing_embed = discord.Embed(
                    title="",
                    description=f"This page trivia is already added to the database. Contact <@756509638169460837> if its wrong!\nIf you want see the facts, check the database in [Github]({fact_list_github}).",
                    colour=discord.Colour(int("ff0000", 16))
                )
                await ctx.respond(embed=existing_embed, ephemeral=True)
        else:
            await ctx.respond(embed=error_embed, ephemeral=True)

    @discord.slash_command(name = "sync_island_fact_github", description = "Add fact of trivia from official Island Wiki")
    async def sync_island_fact_github(self, ctx: discord.ApplicationContext):
        await ctx.defer(ephemeral=True)
        if int(ctx.author.id) != 756509638169460837 and not any(role.id in [
                staff_manager,
                community_manager,
                assistant_director,
                head_of_operations,
                developer,
                mr_boomsteak] for role in ctx.author.roles):
            await ctx.respond(embed=no_perm_embed, ephemeral=True)
            return
        
        # Get the github version
        headers = {'Authorization': f'token {github_token}'}
        response = requests.get(raw_fact_list_github, headers=headers)
        version_prefix = "**Version: "
        version_suffix = "**"
        content = response.text
        lines = content.split('\n')

        # get version
        version_line = next((line for line in lines if line.startswith(version_prefix)), None)
        if version_line is None:
            await ctx.respond("Failed get version in Github.", ephemeral=True)
            return

        github_version = int(version_line.strip().replace(version_prefix, "").replace(version_suffix, ""))

        # Get local version
        with open(facts_md, "r", encoding="utf-8") as f:
            lines = f.readlines()

        version_prefix = "**Version: "
        version_suffix = "**"

        # get version
        version_line = next((line for line in lines if line.startswith(version_prefix)), None)
        if version_line is None:
            await ctx.respond("Failed get local facts version.", ephemeral=True)
            return

        local_version = int(version_line.strip().replace(version_prefix, "").replace(version_suffix, ""))

        if github_version == local_version:
            await ctx.respond("It is already synchronized")

        elif github_version > local_version:
            # Facts list
            r = requests.get(raw_fact_list_github, allow_redirects=True, headers=headers)
            open(facts_md, 'wb').write(r.content)

            # Facts database
            r = requests.get(raw_fact_database_github, allow_redirects=True, headers=headers)
            open(island_fact_database, 'wb').write(r.content)

            # Added facts link
            r = requests.get(raw_added_fact_github, allow_redirects=True, headers=headers)
            open(added_trivia_path, 'wb').write(r.content)
            await ctx.respond("Detected Github facts are newer. Copying from Github to bot local storage.", ephemeral=True)

        elif github_version < local_version:
            push_facts_github('./', [facts_md, added_trivia_path, island_fact_database], f'Update fact data from local v:{local_version}', 'kor', 'https://github.com/Stageddat/kor')
            await ctx.respond("Detected local facts are newer. Uploading from local to Github.", ephemeral=True)
        else:
            await ctx.respond(embed=error_embed, ephemeral=True)

    @discord.Cog.listener()
    async def on_ready(self):
        # dailyfact.start()
        bot.add_view(error_trivia_help())

    print("Loading commands")
    bot.add_application_command(fact_group)


def setup(bot):
    bot.add_cog(fact(bot)) # add the cog to the bot

# DAILY RANDOM FACT HERE
# last_sent = None
# channel = bot.get_channel(934367707212677151)

# def get_fact_number():
#     mydb = pool.get_connection()
#     cursor = mydb.cursor()
#     cursor.execute("SELECT fact_day_number FROM server_variables")
#     result = cursor.fetchone()
#     cursor.close()
#     mydb.close()
#     return int(result[0])

# def increment_fact_number():
#     mydb = pool.get_connection()
#     cursor = mydb.cursor()
#     cursor.execute("UPDATE server_variables SET fact_day_number = fact_day_number + 1")
#     mydb.commit()
#     cursor.close()
#     mydb.close()

# @tasks.loop(seconds=1)
# async def dailyfact():
#     global last_sent
#     now = datetime.now(pytz.utc)
#     cest = pytz.timezone('Europe/Madrid')
#     if now.astimezone(cest).hour == 17 and now.astimezone(cest).minute == 00:
#         # print("ITS TIME FOR NEW!")
#         if last_sent is None or now.date() != last_sent:
#             last_sent = now.date()
#             channel = bot.get_channel(1133869739882586112)
#             fact_type = random.randint(1, 3)
#             if fact_type == 1:
#                 fact = get_randomfact()
#                 print(f'Daily random fact: {fact}')
#                 dailyfact_embed = discord.Embed(
#                     title="Did you know? 🤔",
#                     description=f"{fact}",
#                     colour=discord.Colour(int("6692d7", 16))
#                 )

#             elif fact_type == 2:
#                 fact = get_randomcatfact()
#                 print(f'Daily random cat fact: {fact}')
#                 dailyfact_embed = discord.Embed(
#                     title="Did you know? 🐱",
#                     description=f"{fact}",
#                     colour=discord.Colour(int("ffcc00", 16))
#                 )
#             else:
#                 fact = get_randomdogfact()
#                 print(f'Daily random dog fact: {fact}')
#                 dailyfact_embed = discord.Embed(
#                     title="Did you know? 🐶",
#                     description=f"{fact}",
#                     colour=discord.Colour(int("964B00", 16))
#                 )

#             fact_number = get_fact_number()
#             increment_fact_number()
#             await channel.send(f'## <@&1134794106195955772> Random Fact #{fact_number}\n', embed=dailyfact_embed)
#     else:
#         pass
