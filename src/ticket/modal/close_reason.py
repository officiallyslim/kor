import discord

from src.ticket.utils.builder_request_utils.close_builder_request_ticket import (
    close_ticket,
)


class close_reason(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.InputText(
                label="Reason",
                placeholder="Close reason",
                min_length=1,
                max_length=200,
                style=discord.InputTextStyle.long,
            )
        )

        self.add_item(
            discord.ui.InputText(
                label="Password",
                placeholder="",
                min_length=1,
                max_length=10,
                style=discord.InputTextStyle.short,
                required=False,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        await close_ticket(
            interaction=interaction,
            reason=self.children[0].value,
            ticket_id=None,
            password=self.children[1].value,
        )
