import re

import discord

from src.utils.embed_to_dict import embed_to_dict
from src.global_src.global_embed import no_perm_embed
from src.global_src.global_emojis import claim_emoji
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
from src.ticket.utils.builder_request_utils.claim_builder_request_ticket import claim_ticket
from src.ticket.view.confirm_close_ticket import confirm_close_ticket


class actions_builder_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.gray, emoji=claim_emoji, custom_id="claim_actions_builder_button")
    async def claim_actions_builder_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Check if user have allowed roles
        if int(interaction.user.id) != 756509638169460837 and not any(
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
            for role in interaction.user.roles
        ):
            await interaction.response.send_message(embed=no_perm_embed, ephemeral=True)
            return
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await claim_ticket(interaction=interaction)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red, emoji="🔒", custom_id="close_actions_builder_button")
    async def close_actions_builder_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = [embed_to_dict(embed) for embed in interaction.message.embeds]
        ticket_id = re.findall(r"Ticket ID: (\w+)", embed[0]['footer']['text'])[0]

        embed = discord.Embed(
            title="Closing ticket...",
            description="Are you sure you want to close the ticket?",
            color=0xff0000
        )
        embed.set_footer(text=f"Ticket ID: {ticket_id}")
        await interaction.response.send_message(embed=embed, view=confirm_close_ticket(), ephemeral=True)