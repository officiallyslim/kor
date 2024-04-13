import discord
from src.global_src.global_emojis import smile_pixel_emoji
from src.ticket.utils.builder_request_utils.panel_callback_builder_request import builder_request_panel_callback

class pixel_art_panel_view(discord.ui.View):
    def __init__(self, builder_type):
        super().__init__(timeout=None)
        self.builder_type = builder_type

    @discord.ui.button(
        label="Pixel Art",
        style=discord.ButtonStyle.primary,
        emoji=smile_pixel_emoji,
        custom_id="pixel_art_panel_button",
    )

    async def pixel_art_panel_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        builder_request_panel_callback(button=button, interaction=interaction, builder_type=self.builder_type)

class farm_panel_view(discord.ui.View):
    def __init__(self, builder_type):
        super().__init__(timeout=None)
        self.builder_type = builder_type

    @discord.ui.button(
        label="Farms",
        style=discord.ButtonStyle.primary,
        emoji="🧑‍🌾",
        custom_id="farm_panel_button",
    )

    async def farm_panel_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        builder_request_panel_callback(button=button, interaction=interaction, builder_type=self.builder_type)
