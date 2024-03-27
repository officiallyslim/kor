import discord
from discord.ext import commands

from typing import Union

def create_overwrites(ctx: commands.Context, *objects: Union[discord.Role, discord.Member]):

    overwrites = {
        obj: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True) for obj in objects
    }

    overwrites.setdefault(
        ctx.guild.default_role, discord.PermissionOverwrite(view_channel=False)
    )

    overwrites[ctx.guild.me] = discord.PermissionOverwrite(view_channel=True)

    return overwrites