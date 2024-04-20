import re

import discord

from src.global_src.embed_to_dict import embed_to_dict
from src.ticket.modal.form_builder_request import builder_request_modal
from src.ticket.view.confirm_close_ticket import confirm_close_ticket
from src.global_src.global_embed import error_embed
from src.ticket.utils.builder_request_utils.db_utils.get_db_data_builder_request import get_builder_ticket_type

class form_builder_request_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Fill", style=discord.ButtonStyle.green, emoji="📝", custom_id="fill_form_pixel_art_view")
    async def fill_form_pixel_art_view_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Get ticket ID
        try:
            print(interaction.channel.topic)
            match = re.findall(r"Ticket ID: (\w+)", interaction.channel.topic)
            if match:
                ticket_id = match[0]
        except Exception:
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return

        ticket_type = get_builder_ticket_type(ticket_id=ticket_id)

        modal = builder_request_modal(title="Builder Request Form",name=interaction.user.name, status="new", ticket_type=ticket_type)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red, emoji="🔒", custom_id="close_form_pixel_art_view")
    async def close_form_pixel_art_view(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = [embed_to_dict(embed) for embed in interaction.message.embeds]
        ticket_id = re.findall(r"Ticket ID: (\w+)", embed[0]['footer']['text'])[0]

        embed = discord.Embed(
            title="Closing ticket...",
            description="Are you sure do you want close the ticket?",
            color=0xff0000
        )
        embed.set_footer(text=f"Ticket ID: {ticket_id}")
        await interaction.response.send_message(embed=embed, view=confirm_close_ticket(), ephemeral=True)