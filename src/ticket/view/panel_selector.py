import discord
from src.global_src.global_emojis import smile_pixel_emoji
import json
from src.global_src.global_embed import error_embed
from src.global_src.global_path import pixel_art_panel_embed_path, farm_panel_embed_path
from src.ticket.view.builder_request_views.builder_request_panel import pixel_art_panel_view, farm_panel_view

ticket_panel_embed_dict = {
    "pixel_art": pixel_art_panel_embed_path,
    "farm": farm_panel_embed_path
}

ticket_panel_view_dict = {
    "pixel_art": pixel_art_panel_view,
    "farm": farm_panel_view
}

class panel_selector(discord.ui.View):
    @discord.ui.select(
        placeholder = "Choose panel",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="pixel_art",
                description="",
                emoji=smile_pixel_emoji
            ),
            discord.SelectOption(
                label="farm",
                description=""
            ),
            discord.SelectOption(
                label="TEST4",
                description=""
            )
        ]
    )
    async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        try:
            with open(ticket_panel_embed_dict[select.values[0]], 'r', encoding='utf-8') as f:
                data = json.load(f)

            for embed_info in data['embeds']:
                embed = discord.Embed.from_dict(embed_info)
                await interaction.response.send_message(content="Sending!", ephemeral=True)
                await interaction.channel.send(embed=embed, view=ticket_panel_view_dict[select.values[0]](builder_type=select.values[0]))

        except Exception:
            await interaction.response.send_message(content="Sending!", ephemeral=True)
            await interaction.channel.send(embed=error_embed, ephemeral=True)
