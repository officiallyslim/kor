from config import *
from discord.commands import Option
from commands.fact_commands import fact_group

class fact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name = "change_fact_number", description = "Change the daily fact number")
    async def change_fact_number(self, ctx, number: Option(int, "The next say fact number")): # type: ignore
        if int(ctx.author.id) != 756509638169460837 and not any(role.id in [moderator_role] for role in ctx.author.roles):
            await ctx.respond("You are not allowed to use this command!", ephemeral=True)
            return

        if not float(number).is_integer():
            await ctx.respond("Please enter an integer without decimals!", ephemeral=True)
            return

        f = open("daily_count.txt", "w")
        f.write(f"{number}")
        f.close()

        await ctx.respond(f"The next daily count number set to `{number}`", ephemeral=True)

    @discord.slash_command(name = "add_island_fact", description = "Add new island fact to database")
    async def change_fact_number(self, ctx, fact: Option(str, "Fact about Islands (Roblox)"), img_link: Option(None, "Related image of the fact"), source_link: Option(None, "Source link of the fact")):# type: ignore
        if int(ctx.author.id) != 756509638169460837 and not any(role.id in [moderator_role] for role in ctx.author.roles):
            await ctx.respond("You are not allowed to use this command!", ephemeral=True)
            return

        if not float(number).is_integer():
            await ctx.respond("Please enter an integer without decimals!", ephemeral=True)
            return

        f = open("daily_count.txt", "w")
        f.write(f"{number}")
        f.close()

        await ctx.respond(f"The next daily count number set to `{number}`", ephemeral=True)



    # @discord.Cog.listener()
    # async def on_ready(self):
    #     # dailyfact.start()
    #     print("Loading commands")

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