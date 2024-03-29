import asyncio
import re
from datetime import datetime
import json
import discord

from config import bot
from src.global_src.embed_to_dict import embed_to_dict
from src.global_src.global_embed import claimed_ticket_embed, no_perm_embed
from src.global_src.global_roles import (
    assistant_director_role_id,
    community_manager_role_id,
    developer_role_id,
    head_administration_role_id,
    head_of_operations_role_id,
    junior_administration_role_id,
    mr_boomsteak_role_id,
    mr_boomsteaks_controller_role_id,
    official_administration_role_id,
    pixel_art_role_id,
    senior_administration_role_id,
    staff_manager_role_id,
    trial_administration_role_id,
)
from src.ticket.utils.pixel_art_utils.db_utils.edit_db_pixel_art import (
    edit_db_pixel_art,
)
from src.ticket.utils.pixel_art_utils.db_utils.get_db_data_pixel_art import (
    get_pixel_art_ticket_open_user_id,
    get_pixel_art_channel_id,
    get_pixel_art_welcome_msg
)
from src.ticket.utils.transcript_website import get_transcript
from src.ticket.utils.create_overwrites import create_custom_overwrites


async def unclaim_ticket(interaction: discord.Interaction):
    # Defer
    await interaction.response.defer(ephemeral=True)

    # Check if user have allowed roles
    if int(interaction.user.id) != 756509638169460837 and not any(
        role.id
        in [
            pixel_art_role_id,
            junior_administration_role_id,
            trial_administration_role_id,
            mr_boomsteaks_controller_role_id,
            official_administration_role_id,
            senior_administration_role_id,
            head_administration_role_id,
            staff_manager_role_id,
            community_manager_role_id,
            assistant_director_role_id,
            head_of_operations_role_id,
            developer_role_id,
            mr_boomsteak_role_id,
        ]
        for role in interaction.user.roles
    ):
        await interaction.response.send_message(embed=no_perm_embed, ephemeral=True)
        return

    # Get ticket ID
    embed = [embed_to_dict(embed) for embed in interaction.message.embeds]
    ticket_id = re.findall(r"Ticket ID: (\w+)", embed[0]["footer"]["text"])[0]

    # Get channel ID
    channel_id = get_pixel_art_channel_id(ticket_id=ticket_id)

    # Get open user ID
    open_user_id = get_pixel_art_ticket_open_user_id(ticket_id=ticket_id)

    # Get users and roles
    whoami = interaction.user
    open_user = bot.get_user(open_user_id)
    pixel_art_role = interaction.guild.get_role(pixel_art_role_id)
    mr_boomsteak_role = interaction.guild.get_role(mr_boomsteak_role_id)
    developer_role = interaction.guild.get_role(developer_role_id)
    head_of_operations_role = interaction.guild.get_role(head_of_operations_role_id)
    assistant_director_role = interaction.guild.get_role(assistant_director_role_id)
    community_manager_role = interaction.guild.get_role(community_manager_role_id)
    staff_manager_role = interaction.guild.get_role(staff_manager_role_id)
    head_administration_role = interaction.guild.get_role(head_administration_role_id)
    senior_administration_role = interaction.guild.get_role(senior_administration_role_id)
    official_administration_role = interaction.guild.get_role(official_administration_role_id)
    junior_administration_role = interaction.guild.get_role(junior_administration_role_id)
    trial_administration_role = interaction.guild.get_role(trial_administration_role_id)
    mr_boomsteaks_controller_role = interaction.guild.get_role(mr_boomsteaks_controller_role_id)

    # Set roles perms
    new_overwrites = create_custom_overwrites(
        interaction,
        no_perm_objects=(),
        view_only_objects=(),
        view_and_chat_objects=(
            whoami,
            open_user,
            pixel_art_role,
            mr_boomsteak_role,
            developer_role,
            head_of_operations_role,
            assistant_director_role,
            community_manager_role,
            staff_manager_role,
            head_administration_role,
            senior_administration_role,
            official_administration_role,
            junior_administration_role,
            trial_administration_role,
            mr_boomsteaks_controller_role,
        ),
    )

    # Set new perms
    ticket_channel = bot.get_channel(channel_id)
    for obj, perms in new_overwrites.items():
        await ticket_channel.set_permissions(obj, overwrite=perms)

    # Respond and edit
    await interaction.followup.send("Unclaimed!", ephemeral=True)

    welcome_msg_id, channel_id = get_pixel_art_welcome_msg(ticket_id=ticket_id)
    welcome_msg = await bot.get_channel(channel_id).fetch_message(welcome_msg_id)
    from src.ticket.view.pixel_art_views.actions_pixel_art import actions_pixel_art_view
    await welcome_msg.edit(view=actions_pixel_art_view())

    # Save to database
    edit_db_pixel_art(ticket_id=ticket_id, claim_user_id=None)