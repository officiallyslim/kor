import discord
from src.ticket.modal.close_reason import close_reason

class confirm_close_ticket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.red, emoji="🗑️", custom_id="confirm_close_ticket_button")
    async def confirm_close_ticket_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = close_reason(title="Closing ticket...")
        await interaction.response.send_modal(modal)
