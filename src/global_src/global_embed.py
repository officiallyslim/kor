from config import discord

no_perm_embed = discord.Embed(
    title="",
    description="You are not allowed to use this command!",
    colour=discord.Colour(int("ff0000", 16))
)

soon_embed = discord.Embed(
    title="Soon!",
    description="This command is not available for now. Try again later!",
    colour=discord.Colour(int("ff0000", 16))
)

error_embed = discord.Embed(
    title="Something failed :c",
    description="Please, contact <@756509638169460837> or any moderator/administrator.",
    colour=discord.Colour(int("ff0000", 16))
)

failed_fetch_daily_channel = discord.Embed(
    title="Daily fact channel log not found!",
    description="Failed log mod action becouse daily fact log channel not found",
    colour=discord.Colour(int("ff0000", 16))
)