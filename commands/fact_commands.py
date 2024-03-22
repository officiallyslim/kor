from config import *
from src.facts.get_fact import get_randomfact, get_randomcatfact, get_randomdogfact, get_islandfact

fact_group = discord.SlashCommandGroup("fact", "Send a fact!")

@fact_group.command(name = "random", description = "Get random fact")
async def fact_normal(ctx: discord.ApplicationContext):
    fact = get_randomfact()
    print(f'Random fact: {fact}')
    randomfact_embed = discord.Embed(
        title="Random fact",
        description=f"{fact}",
        colour=discord.Colour(int("6692d7", 16))
    )
    
    await ctx.respond(embed=randomfact_embed)

@fact_group.command(name = "cat", description = "Get random cat fact 😺")
async def cat_fact(ctx: discord.ApplicationContext):
    catfact = get_randomcatfact()
    print(f'Random cat fact: {catfact}')
    randomcatfact_embed = discord.Embed(
        title="Random cat fact 😺",
        description=f"{catfact}",
        colour=discord.Colour(int("ffcc00", 16))
    )

    await ctx.respond(embed=randomcatfact_embed)

@fact_group.command(name = "dog", description = "Get random dog fact 🐶")
async def dog_fact(ctx: discord.ApplicationContext):
    dogfact = get_randomdogfact()
    print(f'Random dog fact: {dogfact}')
    randomdogfact_embed = discord.Embed(
        title="Random dog fact 🐶",
        description=f"{dogfact}",
        colour=discord.Colour(int("964B00", 16))
    )

    await ctx.respond(embed=randomdogfact_embed)

@fact_group.command(name = "island", description = "Get random Island Roblox fact 🏝️")
async def island_fact(ctx: discord.ApplicationContext):
    fact = get_islandfact()
    print(f"Random island fact: {fact['Fact']}")
    randomislandfact_embed = discord.Embed(
        title="Random island fact 🏝️",
        description=f"{fact['Fact']}",
        colour=discord.Colour(int("d1e8fa", 16))
    )
    if fact['Image Link'] != None:
        randomislandfact_embed.set_image(url=f"{str(fact['Image Link'])}")
    if fact["Source Link"] == None:
        await ctx.respond(embed=randomislandfact_embed)
    else:
        await ctx.respond(embed=randomislandfact_embed, view=source_island(fact['Source Link']))

class source_island(discord.ui.View):
    def __init__(self, source_link):
        super().__init__()
        self.add_item(discord.ui.Button(label="Information source", url=f'{source_link}'))

# @fact_group.command(name = "help", description = "Random facts help")
# async def fact_help(ctx: discord.ApplicationContext):
#     await ctx.respond("# Random facts bot help\n**Commands**\n`/help` --> Show this message\n`/randomfact` or `/fact` --> Send a random fact\n`/catfact` --> Send a cat fact\n`/dogfact` --> Send a dog fact\n\nBot developed by <@798463397443403786> and <@756509638169460837>", allowed_mentions=discord.AllowedMentions(users=False))