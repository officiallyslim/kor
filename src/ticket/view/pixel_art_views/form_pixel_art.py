import re

import discord

from src.global_src.embed_to_dict import embed_to_dict
from src.global_src.global_embed import claimed_ticket_embed, no_perm_embed
from src.global_src.global_emojis import claim_emoji
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
from src.ticket.modal.form_pixel_art import form_pixel_art_modal
from src.ticket.utils.db_utils.get_db_data_pixel_art import check_ticket_claimed


class form_pixel_art_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Fill", style=discord.ButtonStyle.green, emoji="📝", custom_id="fill_form_pixel_art_view")
    async def fill_form_pixel_art_view_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = form_pixel_art_modal(title="Pixel Art Form",name=interaction.user.name, status="new")
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.gray, emoji=claim_emoji, custom_id="claim_form_pixel_art_view")
    async def claim_form_pixel_art_view(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red, emoji="🔒", custom_id="close_form_pixel_art_view")
    async def close_form_pixel_art_view(self, button: discord.ui.Button, interaction: discord.Interaction):
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
            if interaction.user.id not in claimed_users_id:
                await interaction.response.send_message(embed=claimed_ticket_embed, ephemeral=True)
                return
        await interaction.response.send_message("Closing ticket...", ephemeral=True)
