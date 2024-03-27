from config import *
from src.global_src.global_path import embed_path
import requests
import json
from src.global_src.global_embed import no_perm_embed
from src.global_src.global_roles import *
from src.ticket.view.pixel_art import pixel_art_panel_view
from src.ticket.view.panel_selector import panel_selector

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

def setup(bot):
    bot.add_cog(ticket(bot))
