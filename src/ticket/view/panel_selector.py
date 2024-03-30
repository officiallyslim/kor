import discord
from src.global_src.global_emojis import smile_pixel_emoji
import json

from src.global_src.global_path import pixel_art_panel_embed_path
from src.ticket.view.pixel_art_views.pixel_art_panel import pixel_art_panel_view

class panel_selector(discord.ui.View):
    @discord.ui.select(
        placeholder = "Choose panel",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="Request A Pixel Art Builder",
                description="",
                emoji=smile_pixel_emoji
            ),
            discord.SelectOption(
                label="TEST2",
                description=""
            ),
            discord.SelectOption(
                label="TEST4",
                description=""
            )
        ]
    )
    async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        if select.values[0] == 'Request A Pixel Art Builder':
            await interaction.response.edit_message(view=panel_selector())
            await interaction.followup.send("Sending...", ephemeral=True)

            with open(pixel_art_panel_embed_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for embed_info in data['embeds']:
                embed = discord.Embed.from_dict(embed_info)

                await interaction.channel.send(embed=embed, view=pixel_art_panel_view())

        else:
            await interaction.response.send_message("SOON!", ephemeral=True)