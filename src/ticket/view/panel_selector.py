import json

import discord

from src.global_src.global_embed import error_embed
from src.global_src.global_emojis import smile_pixel_emoji
from src.global_src.global_path import (
    farm_panel_embed_path,
    industrial_panel_embed_path,
    pixel_art_panel_embed_path,
    strucure_panel_embed_path,
    shop_panel_embed_path,
    expo_demo_panel_embed_path
)
from src.ticket.view.builder_request_views.builder_request_panel import (
    builder_panel_view,
)

ticket_panel_embed_dict = {
    "pixel_art": pixel_art_panel_embed_path,
    "farm": farm_panel_embed_path,
    "structure": strucure_panel_embed_path,
    "industrial": industrial_panel_embed_path,
    "shop": shop_panel_embed_path,
    "expo/demo": expo_demo_panel_embed_path
}

class panel_selector(discord.ui.View):
    @discord.ui.select(
        placeholder="Choose panel",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="Send all",
                description="Send all panels",
                emoji="📤"
            ),
            discord.SelectOption(
                label="pixel_art",
                description="",
                emoji=smile_pixel_emoji
            ),
            discord.SelectOption(
                label="farm",
                description="",
                emoji="🧑‍🌾"
            ),
            discord.SelectOption(
                label="structure",
                description="",
                emoji="🏠"
            ),
            discord.SelectOption(
                label="industrial",
                description="",
                emoji="🏭"
            ),
            discord.SelectOption(
                label="shop",
                description="",
                emoji="🛒"
            ),
            discord.SelectOption(
                label="expo/demo",
                description="",
                emoji="⚒️"
            )
        ]
    )
    async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        if select.values[0] == "Send all":
            await interaction.response.send_message(content="Sending all panels!", ephemeral=True)
            for label, file_path in ticket_panel_embed_dict.items():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    for embed_info in data['embeds']:
                        embed = discord.Embed.from_dict(embed_info)
                        await interaction.channel.send(embed=embed, view=builder_panel_view())
                except Exception as e:
                    print(e)
                    await interaction.followup.send(embed=error_embed, ephemeral=True)
        else:
            try:
                with open(ticket_panel_embed_dict[select.values[0]], 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for embed_info in data['embeds']:
                    embed = discord.Embed.from_dict(embed_info)
                    await interaction.response.send_message(content="Sending!", ephemeral=True)
                    await interaction.channel.send(embed=embed, view=builder_panel_view())
            except Exception as e:
                print(e)
                await interaction.followup.send(embed=error_embed, ephemeral=True)