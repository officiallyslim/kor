import discord
from discord.ext import commands

from typing import Union

def create_custom_overwrites(
    ctx: commands.Context,
    no_perm_objects: Union[discord.Role, discord.Member],
    view_only_objects: Union[discord.Role, discord.Member],
    view_and_chat_objects: Union[discord.Role, discord.Member]
):

    overwrites = {}

    # no perm
    for obj in no_perm_objects:
        overwrites[obj] = discord.PermissionOverwrite(view_channel=False)

    # Only view perm
    for obj in view_only_objects:
        overwrites[obj] = discord.PermissionOverwrite(
            view_channel=True,
            send_messages=False,
            send_messages_in_threads=False,
            create_public_threads=False,
            create_private_threads=False,
            attach_files=False,
            read_messages=True,
            read_message_history=True,
        )

    # View and chat perm
    for obj in view_and_chat_objects:
        overwrites[obj] = discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            send_messages_in_threads=False,
            create_public_threads=False,
            create_private_threads=False,
            attach_files=True,
            read_messages=True,
            read_message_history=True,
        )

    # @everyone perm
    overwrites.setdefault(
        ctx.guild.default_role, discord.PermissionOverwrite(view_channel=False)
    )

    # Bot perm
    # overwrites[ctx.guild.me] = discord.PermissionOverwrite(view_channel=True)

    return overwrites

def create_view_only_overwrites(
    ctx: commands.Context, *objects: Union[discord.Role, discord.Member]
):

    overwrites = {
        obj: discord.PermissionOverwrite(
            view_channel=True,
            send_messages=False,
            send_messages_in_threads=False,
            create_public_threads=False,
            create_private_threads=False,
            attach_files=True,
            read_messages=True,
            read_message_history=True,
        )
        for obj in objects
    }

    overwrites.setdefault(
        ctx.guild.default_role, discord.PermissionOverwrite(view_channel=False)
    )

    # overwrites[ctx.guild.me] = discord.PermissionOverwrite(view_channel=True)

    return overwrites

def create_view_and_chat_overwrites(
    ctx: commands.Context, *objects: Union[discord.Role, discord.Member]
):

    overwrites = {
        obj: discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            send_messages_in_threads=False,
            create_public_threads=False,
            create_private_threads=False,
            attach_files=True,
            read_messages=True,
            read_message_history=True,
        )
        for obj in objects
    }

    overwrites.setdefault(
        ctx.guild.default_role, discord.PermissionOverwrite(view_channel=False)
    )

    # overwrites[ctx.guild.me] = discord.PermissionOverwrite(view_channel=True)

    return overwrites

def create_no_perm_overwrites(
    ctx: commands.Context, *objects: Union[discord.Role, discord.Member]
):

    overwrites = {
        obj: discord.PermissionOverwrite(
            view_channel=False,
        )
        for obj in objects
    }

    overwrites.setdefault(
        ctx.guild.default_role, discord.PermissionOverwrite(view_channel=False)
    )

    # overwrites[ctx.guild.me] = discord.PermissionOverwrite(view_channel=True)

    return overwrites
