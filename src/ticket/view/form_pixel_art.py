import discord
from src.ticket.modal.form_pixel_art import form_pixel_art_modal

class form_pixel_art_view(discord.ui.View):
    @discord.ui.button(label="Fill", style=discord.ButtonStyle.green, emoji="✏️")
    async def button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = form_pixel_art_modal(title="Pixel Art Form",name=interaction.user.name)
        await interaction.response.send_modal(modal)