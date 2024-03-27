import discord
from src.global_src.global_emojis import smile_pixel_emoji

class pixel_art_panel_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Pixel Art", style=discord.ButtonStyle.primary, emoji=smile_pixel_emoji, custom_id="pixel_art_panel_button")
    async def pixel_art_panel_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("SOON!", ephemeral=True)