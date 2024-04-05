import re

import discord

from src.global_src.embed_to_dict import embed_to_dict
from src.global_src.global_emojis import claim_emoji
from src.ticket.utils.builder_request_utils.unclaim_builder_request_ticket import unclaim_ticket
from src.ticket.view.confirm_close_ticket import confirm_close_ticket
from src.ticket.utils.builder_request_utils.db_utils.get_db_data_builder_request import check_claimed_pixeL_art_ticket

class actions_claimed_pixel_art_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Unclaim", style=discord.ButtonStyle.gray, emoji=claim_emoji, custom_id="claim_claimed_actions_pixel_art_button")
    async def claim_claimed_actions_pixel_art_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Get ticket_id
        embed = [embed_to_dict(embed) for embed in interaction.message.embeds]
        ticket_id = re.findall(r"Ticket ID: (\w+)", embed[0]["footer"]["text"])[0]

        # Check if user is the claimer
        claim_user_id = check_claimed_pixeL_art_ticket(ticket_id)
        if claim_user_id is not None:
            if interaction.user.id != claim_user_id:
                await interaction.response.send_message("Sorry, only claim user can unclaim.", ephemeral=True)
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await unclaim_ticket(interaction=interaction)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red, emoji="🔒", custom_id="close_claimed_actions_pixel_art_button")
    async def close_claimed_actions_pixel_art_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = [embed_to_dict(embed) for embed in interaction.message.embeds]
        ticket_id = re.findall(r"Ticket ID: (\w+)", embed[0]['footer']['text'])[0]

        embed = discord.Embed(
            title="Closing ticket...",
            description="Are you u want close the ticket?",
            color=0xff0000
        )
        embed.set_footer(text=f"Ticket ID: {ticket_id}")
        await interaction.response.send_message(embed=embed, view=confirm_close_ticket(), ephemeral=True)