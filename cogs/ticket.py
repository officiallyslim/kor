import asyncio

import discord
from discord.ext import commands

from config import bot, guild_id
from src.global_src.global_embed import no_perm_embed
from src.global_src.global_roles import (
    assistant_director,
    community_manager,
    developer,
    head_of_operations,
    mr_boomsteak,
    staff_manager,
)
from src.ticket.utils.is_message_from_ticket import is_message_from_ticket
from src.ticket.utils.transcript_webhook import transcript
from src.ticket.view.confirm_form_pixel_art import confirm_form_pixel_art_view
from src.ticket.view.form_pixel_art import form_pixel_art_view
from src.ticket.view.panel_selector import panel_selector
from src.ticket.view.pixel_art import pixel_art_panel_view
from src.ticket.view.actions_pixel_art import actions_pixel_art_view


class ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name = "send_panel", description = "Send embed in specifically channel")
    async def embed_sender(self, ctx: discord.ApplicationContext):
        if int(ctx.author.id) != 756509638169460837 and not any(role.id in [staff_manager, community_manager, assistant_director, head_of_operations, developer, mr_boomsteak] for role in ctx.author.roles):
            await ctx.respond(embed=no_perm_embed, ephemeral=True)
            return
        await ctx.respond("Select a panel",view=panel_selector(), ephemeral=True)

    @discord.Cog.listener()
    async def on_ready(self):
        bot.add_view(pixel_art_panel_view())
        bot.add_view(form_pixel_art_view())
        bot.add_view(confirm_form_pixel_art_view())
        bot.add_view(actions_pixel_art_view())

    @discord.Cog.listener()
    async def on_message(self, message: discord.Message):
        if isinstance(message.channel, discord.DMChannel):
            return
        if message.guild.id != guild_id:
            return

        if is_message_from_ticket(message.channel.id):
            await transcript(message)
        else:
            await asyncio.sleep(1)
            if is_message_from_ticket(message.channel.id):
                await transcript(message)


def setup(bot):
    bot.add_cog(ticket(bot))
