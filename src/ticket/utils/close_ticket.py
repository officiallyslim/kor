import re

import discord

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
from src.ticket.utils.db_utils.get_db_data_pixel_art import check_ticket_claimed


async def close_ticket(button: discord.ui.Button, interaction: discord.Interaction):
        # Check if user have allowed roles
    if int(interaction.user.id) != 756509638169460837 and not any(role.id in [
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
            mr_boomsteak_role_id] for role in interaction.user.roles):
        await interaction.response.send_message(embed=no_perm_embed, ephemeral=True)
        return

    # Get ticket ID
    embed = [embed_to_dict(embed) for embed in interaction.message.embeds]
    ticket_id = re.findall(r"Ticket ID: (\w+)", embed[0]['footer']['text'])[0]

    # Check if user is in claimed user for close
    claimed_users_id = check_ticket_claimed(ticket_id)
    if claimed_users_id is not None:
        print(claimed_users_id)
        if interaction.user.id not in claimed_users_id:
            await interaction.response.send_message(embed=claimed_ticket_embed, ephemeral=True)
            return

    await interaction.response.send_message("Closing ticket...", ephemeral=True)
