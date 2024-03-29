import re

import discord

from src.global_src.embed_to_dict import embed_to_dict
from src.global_src.global_emojis import claim_emoji
from src.ticket.modal.form_pixel_art import form_pixel_art_modal
from src.ticket.view.confirm_close_ticket import confirm_close_ticket
from src.ticket.utils.pixel_art_utils.claim_pixel_art_ticket import claim_ticket


class form_pixel_art_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Fill", style=discord.ButtonStyle.green, emoji="📝", custom_id="fill_form_pixel_art_view")
    async def fill_form_pixel_art_view_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = form_pixel_art_modal(title="Pixel Art Form",name=interaction.user.name, status="new")
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.gray, emoji=claim_emoji, custom_id="claim_form_pixel_art_view")
    async def claim_form_pixel_art_view(self, button: discord.ui.Button, interaction: discord.Interaction):
        await claim_ticket(interaction=interaction)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red, emoji="🔒", custom_id="close_form_pixel_art_view")
    async def close_form_pixel_art_view(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = [embed_to_dict(embed) for embed in interaction.message.embeds]
        ticket_id = re.findall(r"Ticket ID: (\w+)", embed[0]['footer']['text'])[0]

        embed = discord.Embed(
            title="Closing ticket...",
            description="Are you u want close the ticket?"
        )
        embed.set_footer(text=f"Ticket ID: {ticket_id}")
        await interaction.response.send_message(embed=embed, view=confirm_close_ticket())