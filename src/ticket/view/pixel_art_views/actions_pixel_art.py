import discord
from src.ticket.modal.form_pixel_art import form_pixel_art_modal
from src.global_src.global_emojis import claim_emoji

class actions_pixel_art_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.gray, emoji=claim_emoji, custom_id="claim_actions_pixel_art_view")
    async def claim_actions_pixel_art_view(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = form_pixel_art_modal(title="Pixel Art Form",name=interaction.user.name)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red, emoji="🔒", custom_id="close_actions_pixel_art_view")
    async def close_actions_pixel_art_view(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = form_pixel_art_modal(title="Pixel Art Form",name=interaction.user.name)
        await interaction.response.send_modal(modal)