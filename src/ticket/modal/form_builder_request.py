
import asyncio

import discord

from config import bot, guild_id
from src.global_src.global_emojis import loading_emoji
from src.ticket.utils.builder_request_utils.db_utils.edit_db_builder_request import (
    edit_builder_request_db,
)
from src.ticket.utils.builder_request_utils.db_utils.get_db_data_builder_request import (
    check_open_builder_ticket,
    get_builder_confirm_message_id,
    get_builder_welcome_msg,
)
from src.ticket.view.builder_request_views.confirm_form_builder_request import (
    confirm_form_builder_view,
)
from src.ticket.view.jump_channel import jump_channel


class builder_request_modal(discord.ui.Modal):
    def __init__(self, ticket_type, roblox_user=None, island_code=None, build=None, status=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.status = status
        self.ticket_type = ticket_type

        self.add_item(discord.ui.InputText(
            label="Roblox username",
            placeholder="Your roblox username",
            min_length = 1,
            max_length = 30,
            style=discord.InputTextStyle.short,
            value=roblox_user,
            row=0
            ))

        self.add_item(discord.ui.InputText(
            label="Island code",
            placeholder="Your Roblox Island Code",
            min_length = 1,
            max_length = 10,
            style=discord.InputTextStyle.short,
            value=island_code,
            row=1
            ))

        self.add_item(discord.ui.InputText(
            label="What build you need?",
            placeholder="What build is in your mind?",
            min_length = 1,
            max_length = 400,
            row=3,
            style=discord.InputTextStyle.long,
            value=build,
            ))

        self.add_item(discord.ui.InputText(
            label="Payment",
            placeholder="Payment price (1B, 1T,...)",
            min_length = 1,
            max_length = 30,
            style=discord.InputTextStyle.short,
            row=4
            ))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Form answers",
            description="",
            color=0x28a745
            )

        embed.add_field(name="User", value=f"```{interaction.user.mention} ({interaction.user.id} - {interaction.user.global_name})```", inline=False)
        embed.add_field(name="Roblox username", value=f"```{self.children[0].value}```", inline=False)
        embed.add_field(name="Island Code", value=f"```{self.children[1].value}```", inline=False)
        embed.add_field(name="Build", value=f"```{self.children[2].value}```", inline=False)
        embed.add_field(name="Payment", value=f"```{self.children[3].value}```", inline=False)
        embed.set_footer(text="Please, confirm your answer before send to builder team.")

        open_ticket = check_open_builder_ticket(int(interaction.user.id), ticket_type=self.ticket_type)
        if open_ticket is False:
            loading_message = await interaction.response.send_message(f"{loading_emoji} Processing...", ephemeral=True)
            await asyncio.sleep(5)
            open_ticket = check_open_builder_ticket(int(interaction.user.id), ticket_type=self.ticket_type)
            ticket_id, channel_id = open_ticket
            await loading_message.edit(content="Please, go to the ticket channel for proceed.", view=jump_channel(guild_id=guild_id, channel_id=channel_id))
        else:
            ticket_id, channel_id = open_ticket

        # Send form or edit
        if self.status == "new": # Send the message if is new form and change view in original welcome message
            welcome_msg_id, channel_id = get_builder_welcome_msg(ticket_id)
            welcome_msg = await bot.get_channel(channel_id).fetch_message(welcome_msg_id)

            from src.ticket.view.builder_request_views.actions_builder_request import (
                actions_builder_view,
            )
            await welcome_msg.edit(view=actions_builder_view())
            confirm_message = await welcome_msg.reply(content="", embed=embed, view=confirm_form_builder_view())
            edit_builder_request_db(ticket_id=ticket_id, confirm_message_id=confirm_message.id)
            try:
                await interaction.response.send_message("Please, go to the ticket channel for proceed", ephemeral=True, view=jump_channel(guild_id, channel_id))
            except Exception:
                pass

        elif self.status == "edit": # Edit if is trying edit the form
            confirm_message_id = get_builder_confirm_message_id(ticket_id)
            confirm_message = await bot.get_channel(channel_id).fetch_message(confirm_message_id)
            await confirm_message.edit(content="", embed=embed, view=confirm_form_builder_view())
            await interaction.response.defer()
            return
