from config import *
import os
import traceback
import dotenv

dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

cogs = ['cogs.fact', 'cogs.embed_sender']

for cog in cogs:
    try:
        bot.load_extension(cog)
        print(f"Cog loaded \"{cog}\"")
    except Exception:
        e = traceback.format_exc()
        print(f"Error loading cog: \"{cog}\": {e}")

@bot.event
async def on_ready():
    print(f"{bot.user} is not dead lol!")
    # await bot.change_presence(activity=discord.Game(name=""))

async def get_cog_names(ctx: discord.AutocompleteContext):
    name = ctx.options['name']
    return [cog for cog in cogs if name.lower() in cog.lower()]

@bot.slash_command(name="reload_cog", description="Reload a specific cog")
async def reload_cog(
    ctx: discord.ApplicationContext,
    name: discord.Option(str, "Cog name to reload", autocomplete=get_cog_names) # type: ignore
):
    if ctx.author.id in admins:
        if name.lower() in cogs:
            try:
                bot.reload_extension(name.lower())
                await ctx.respond(f"Cog \"{name}\" reloaded correctly")
            except:
                await ctx.respond(f"Failed to reload cog \"{name}\"")
            return
        await ctx.respond(f"I can't find \"{name}\" :c")
    else:
        await ctx.respond("You are not allowed to use this command")

bot.run(token)
