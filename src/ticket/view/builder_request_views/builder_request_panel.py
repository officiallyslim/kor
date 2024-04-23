import discord

from src.global_src.embed_to_dict import embed_to_dict
from src.ticket.utils.builder_request_utils.builder_ticket_type import ticket_type_dict
from src.ticket.utils.builder_request_utils.panel_callback_builder_request import (
    builder_request_panel_callback,
)

    # "⚒️Request an Expo/Demo worker ⚒️": "expodemo_worker",
    # "🤖Request A Industrial Builder🤖": "industrial",
    # "🛒Request a Shop Builder🛒": "shop"

class builder_panel_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Setting up!",
        style=discord.ButtonStyle.red,
        emoji="🚀",
        custom_id="builder_panel_button",
    )

    async def builder_panel_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = [embed_to_dict(embed) for embed in interaction.message.embeds]
        ticket_title = embed[0]['title']
        ticket_data = ticket_type_dict[ticket_title]

        if button.label == "Setting up!":
            button.label = ticket_data['button_label']
            button.emoji = ticket_data['emoji']
            button.style = discord.ButtonStyle.grey

            await interaction.response.edit_message(view=self)
            await interaction.followup.send("Starting...\nPlease click again to create a ticket.", ephemeral=True)
            return
        else:
            await builder_request_panel_callback(button=button, interaction=interaction, builder_type=ticket_data['type'])