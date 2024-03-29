import asyncio

import discord
from discord.ext import commands

from config import bot, guild_id
from src.global_src.global_embed import no_perm_embed
from src.global_src.global_roles import (
    assistant_director_role_id,
    community_manager_role_id,
    developer_role_id,
    head_of_operations_role_id,
    mr_boomsteak_role_id,
    staff_manager_role_id,
)
from src.ticket.utils.is_message_from_ticket import is_message_from_ticket
from src.ticket.view.confirm_close_ticket import confirm_close_ticket
from src.ticket.view.panel_selector import panel_selector
from src.ticket.view.pixel_art_views.actions_claimed_pixel_art import (
    actions_claimed_pixel_art_view,
)
from src.ticket.view.pixel_art_views.actions_pixel_art import actions_pixel_art_view
from src.ticket.view.pixel_art_views.confirm_form_pixel_art import (
    confirm_form_pixel_art_view,
)
from src.ticket.view.pixel_art_views.form_pixel_art import form_pixel_art_view
from src.ticket.view.pixel_art_views.pixel_art_panel import pixel_art_panel_view


class ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name = "send_panel", description = "Send embed in specifically channel")
    async def embed_sender(self, ctx: discord.ApplicationContext):
        if int(ctx.author.id) != 756509638169460837 and not any(role.id in [staff_manager_role_id, community_manager_role_id, assistant_director_role_id, head_of_operations_role_id, developer_role_id, mr_boomsteak_role_id] for role in ctx.author.roles):
            await ctx.respond(embed=no_perm_embed, ephemeral=True)
            return
        await ctx.respond("Select a panel",view=panel_selector(), ephemeral=True)

    @discord.Cog.listener()
    async def on_ready(self):
        bot.add_view(pixel_art_panel_view())
        bot.add_view(form_pixel_art_view())
        bot.add_view(confirm_form_pixel_art_view())
        bot.add_view(actions_pixel_art_view())
        bot.add_view(confirm_close_ticket())
        bot.add_view(actions_claimed_pixel_art_view())

def setup(bot):
    bot.add_cog(ticket(bot))
