import discord
from src.loa_request.utils.get_max_role import get_max_builder, get_max_moderator


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
        author_roles = interaction.user.roles
        max_role = get_max_moderator(author_roles)
        if max_role == "No moderator role":
            max_role = get_max_builder(author_roles)
            if max_role == "No builder role":
                await interaction.response.send_message("You are not moderator and builder.", ephemeral=True)
                return
        await interaction.response.send_message(f"According to my dumb brain, your max role is: `{max_role}`", ephemeral=True)
