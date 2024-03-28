import re

import discord

from config import bot
from src.ticket.utils.db_utils.get_db_data_pixel_art import get_welcome_msg
from src.ticket.view.pixel_art_views.confirm_form_pixel_art import confirm_form_pixel_art_view


class form_pixel_art_modal(discord.ui.Modal):
    def __init__(self, name, roblox_user=None, island_code=None, build=None, status=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.status = status

        self.add_item(discord.ui.InputText(
            label="Discord name",
            placeholder="Your discord name",
            min_length = 1,
            max_length = 30,
            style=discord.InputTextStyle.short,
            value=name
            ))

        self.add_item(discord.ui.InputText(
            label="Roblox username",
            placeholder="Your roblox username",
            min_length = 1,
            max_length = 30,
            style=discord.InputTextStyle.short,
            value=roblox_user
            ))

        self.add_item(discord.ui.InputText(
            label="Island code",
            placeholder="Your Roblox Island Code",
            min_length = 1,
            max_length = 10,
            style=discord.InputTextStyle.short,
            value=island_code
            ))

        self.add_item(discord.ui.InputText(
            label="What build you need?",
            placeholder="What build is in your mind?",
            min_length = 1,
            max_length = 400,
            row=3,
            style=discord.InputTextStyle.long,
            value=build
            ))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Pixel Art form answers",
            description="",
            color=0x28a745
            )

        embed.add_field(name="Discord name", value=f"```{self.children[0].value}```", inline=False)
        embed.add_field(name="Roblox username", value=f"```{self.children[1].value}```", inline=False)
        embed.add_field(name="Island Code", value=f"```{self.children[2].value}```", inline=False)
        embed.add_field(name="Build", value=f"```{self.children[3].value}```", inline=False)

        # Send form or edit
        if self.status == "new": # Send the message if is new form and change view in original welcome message
            await interaction.response.send_message(content="Please, confirm your answer before send to moderators", embed=embed, view=confirm_form_pixel_art_view())
            ticket_id = re.findall(r"Ticket ID: (\w+)", interaction.channel.topic)[0]
            welcome_msg_id, channel_id = get_welcome_msg(ticket_id)
            welcome_msg = await bot.get_channel(channel_id).fetch_message(welcome_msg_id)

            from src.ticket.view.pixel_art_views.actions_pixel_art import actions_pixel_art_view
            await welcome_msg.edit(view=actions_pixel_art_view())

        elif self.status == "edit": # Edit if is trying edit the form
            await interaction.response.edit_message(content="Please, confirm your answer before send to moderators", embed=embed, view=confirm_form_pixel_art_view())