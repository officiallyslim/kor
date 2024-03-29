import re

import discord

from src.global_src.embed_to_dict import embed_to_dict
from src.global_src.global_emojis import claim_emoji
from src.ticket.view.confirm_close_ticket import confirm_close_ticket


class actions_pixel_art_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.gray, emoji=claim_emoji, custom_id="claim_actions_pixel_art_button")
    async def claim_actions_pixel_art_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red, emoji="🔒", custom_id="close_actions_pixel_art_button")
    async def close_actions_pixel_art_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = [embed_to_dict(embed) for embed in interaction.message.embeds]
        ticket_id = re.findall(r"Ticket ID: (\w+)", embed[0]['footer']['text'])[0]

        embed = discord.Embed(
            title="Closing ticket...",
            description="Are you u want close the ticket?"
        )
        embed.set_footer(text=f"Ticket ID: {ticket_id}")
        await interaction.response.send_message(embed=embed, view=confirm_close_ticket())