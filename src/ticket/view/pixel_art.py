import discord
from src.global_src.global_emojis import smile_pixel_emoji
from src.ticket.utils.create_overwrites import create_overwrites
from typing import Union
from src.ticket.utils.gen_ticket_key import gen_key
from datetime import datetime

class pixel_art_panel_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Pixel Art", style=discord.ButtonStyle.primary, emoji=smile_pixel_emoji, custom_id="pixel_art_panel_button")
    async def pixel_art_panel_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        ticket_id = gen_key(15)
        print(f"Creating new ticket: {ticket_id}")

        whoami = interaction.user
        mod_role = interaction.guild.get_role(1222579667207192626)

        objects = (whoami, mod_role)

        overwrites = create_overwrites(interaction, *objects)

        new_channel = await interaction.guild.create_text_channel(
            name=f"{interaction.user.name} - pixel",
            overwrites=overwrites,
            topic=f"{interaction.user.name} Pixel Art Builder request\n Created at <t:{int(datetime.now().timestamp())}>",
            reason="New channel for Pixel Art Builder request",
            category=discord.Object(id=1222316215884582924)
        )
        channel_id = new_channel.id
        await new_channel.send("Welcome pookie lmao")
