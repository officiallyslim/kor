import re
from config import bot
import discord

from src.global_src.global_embed import no_perm_embed

from src.global_src.global_roles import (
    expo_role_id,
    farm_role_id,
    giveaway_role_id,
    industrial_role_id,
    pixel_art_role_id,
    recruitment_role_id,
    shop_role_id,
    structure_role_id,
    support_role_id,
)
from src.ticket.utils.create_overwrites import create_no_perm_overwrites, create_view_and_chat_overwrites
from src.ticket.utils.builder_request_utils.db_utils.get_db_data_builder_request import get_builder_channel_id
ticket_group = discord.SlashCommandGroup("ticket", "Ticket utils command")

@ticket_group.command(name = "add", description = "Add someone to the current ticket channel")
async def add_user_ticket(ctx: discord.ApplicationContext, user: discord.Member):
    if int(ctx.user.id) != 756509638169460837 and not any(role.id in [
            pixel_art_role_id,
            expo_role_id,
            shop_role_id,
            industrial_role_id,
            farm_role_id,
            structure_role_id,
            recruitment_role_id,
            support_role_id,
            giveaway_role_id,
        ]
        for role in ctx.user.roles
    ):
        await ctx.response.send_message(embed=no_perm_embed, ephemeral=True)
        return

    # Get ticket ID
    try:
        ticket_id = re.findall(r"Ticket ID: (\w+)", ctx.channel.topic)
    except Exception:
        ticket_id = None

    if ticket_id is None:
        await ctx.response.send_message("Sorry, you need be in the same ticket channel for add someone new!", ephemeral=True)
        return

    # Get datas
    ticket_channel_id = get_builder_channel_id(ticket_id[0])

    # Set new perms
    new_overwrites = create_view_and_chat_overwrites(ctx, user)
    ticket_channel = bot.get_channel(ticket_channel_id)
    await ticket_channel.set_permissions(user, overwrite=new_overwrites[user])
    await ctx.response.send_message(f"{user.mention} added correctly!", ephemeral=True)

@ticket_group.command(name = "remove", description = "Remove someone to the current ticket channel")
async def remove_user_ticket(ctx: discord.ApplicationContext, user: discord.Member):
    if int(ctx.user.id) != 756509638169460837 and not any(role.id in [
            pixel_art_role_id,
            expo_role_id,
            shop_role_id,
            industrial_role_id,
            farm_role_id,
            structure_role_id,
            recruitment_role_id,
            support_role_id,
            giveaway_role_id,
        ]
        for role in ctx.user.roles
    ):
        await ctx.response.send_message(embed=no_perm_embed, ephemeral=True)
        return

    # Get ticket ID
    try:
        ticket_id = re.findall(r"Ticket ID: (\w+)", ctx.channel.topic)
    except Exception:
        ticket_id = None

    if ticket_id is None:
        await ctx.response.send_message("Sorry, you need be in the same ticket channel for remove someone!", ephemeral=True)
        return

    # Get datas
    ticket_channel_id = get_builder_channel_id(ticket_id[0])

    # Set new perms
    new_overwrites = create_no_perm_overwrites(ctx, user)
    ticket_channel = bot.get_channel(ticket_channel_id)
    await ticket_channel.set_permissions(user, overwrite=new_overwrites[user])
    await ctx.response.send_message(f"{user.mention} removed correctly!", ephemeral=True)