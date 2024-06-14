import re

import discord

from config import bot
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
from src.ticket.utils.builder_request_utils.db_utils.get_db_data_builder_request import (
    check_claimed_builder_ticket,
    get_builder_channel_id,
    get_builder_open_user_id,
)
from src.ticket.utils.create_overwrites import (
    create_no_perm_overwrites,
)


async def remove_user_ticket(ctx: discord.ApplicationContext, user: discord.Member):
    if int(ctx.user.id) != 756509638169460837 and not any(
        role.id
        in [
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
        await ctx.response.send_message(
            "Sorry, you need be in the same ticket channel for remove someone!",
            ephemeral=True,
        )
        return

    # Deny remove claim user
    claim_user_id = check_claimed_builder_ticket(ticket_id[0])
    if claim_user_id is not None:
        if user.id == claim_user_id:
            await ctx.response.send_message("You cant remove claim user.", ephemeral=True)
            return

    # Deny remove open user
    open_user_id = get_builder_open_user_id(ticket_id[0])
    if open_user_id is not None:
        if user.id == open_user_id:
            await ctx.response.send_message("You cant remove open user.", ephemeral=True)
            return

    # Get datas
    ticket_channel_id = get_builder_channel_id(ticket_id[0])

    # Set new perms
    new_overwrites = create_no_perm_overwrites(ctx, user)
    ticket_channel = bot.get_channel(ticket_channel_id)
    await ticket_channel.set_permissions(user, overwrite=new_overwrites[user])
    await ctx.response.send_message(
        f"{user.mention} removed correctly!", ephemeral=True
    )