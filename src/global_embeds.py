from config import discord

no_perm_embed = discord.Embed(
    title="",
    description=f"You are not allowed to use this command!",
    colour=discord.Colour(int("ff0000", 16))
)

soon_embed = discord.Embed(
    title="Soon!",
    description=f"This command is not available for now. Try again later!",
    colour=discord.Colour(int("ff0000", 16))
)

error_embed = discord.Embed(
    title="Something failed :c",
    description=f"Please, contact <@756509638169460837> or any moderator/administrator.",
    colour=discord.Colour(int("ff0000", 16))
)