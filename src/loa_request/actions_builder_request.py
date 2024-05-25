import discord


class loa_request_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Request",
        style=discord.ButtonStyle.green,
        emoji="😩",
        custom_id="request_loa_callback",
    )
    async def request_loa_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        pass
