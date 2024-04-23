
import discord
from discord.ext import commands

from commands.ticket_commands import ticket_group
from config import bot
from src.global_src.global_embed import no_perm_embed
from src.global_src.global_roles import (
    assistant_director_role_id,
    community_manager_role_id,
    developer_role_id,
    head_of_operations_role_id,
    mr_boomsteak_role_id,
    staff_manager_role_id,
)
from src.ticket.view.confirm_close_ticket import confirm_close_ticket
from src.ticket.view.panel_selector import panel_selector
from src.ticket.view.builder_request_views.actions_claimed_builder_request import (
    actions_claimed_pixel_art_view,
)
from src.ticket.view.builder_request_views.actions_builder_request import actions_builder_view
from src.ticket.view.builder_request_views.confirm_form_builder_request import (
    confirm_form_builder_view,
)
from src.ticket.view.builder_request_views.form_builder_request import form_builder_request_view
from src.ticket.view.builder_request_views.builder_request_panel import builder_panel_view


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
        bot.add_view(builder_panel_view())
        bot.add_view(form_builder_request_view())
        bot.add_view(confirm_form_builder_view())
        bot.add_view(actions_builder_view())
        bot.add_view(confirm_close_ticket())
        bot.add_view(actions_claimed_pixel_art_view())

    print("Loading ticket commands...")
    bot.add_application_command(ticket_group)
    print("Ticket commands loaded!")

def setup(bot):
    bot.add_cog(ticket(bot))
