
import discord

from src.ticket.utils.close_ticket import close_ticket


class close_reason(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(
            label="Reason",
            placeholder="Close reason",
            min_length = 1,
            max_length = 30,
            style=discord.InputTextStyle.short,
            ))

    async def callback(self, interaction: discord.Interaction):
        await close_ticket(interaction=interaction, reason=self.children[0].value)