import discord
from discord.ext import commands

from config import bot
from src.global_src.global_embed import no_perm_embed
from src.global_src.global_roles import (
    assistant_director_role_id,
    community_manager_role_id,
    developer_role_id,
    head_of_operations_role_id,
    owner_role_id,
    staff_manager_role_id,
)


class bss_codes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="force_bss_scrap", description="Force scrap BSS codes"
    )
    async def force_bss_scrap(self, ctx: discord.ApplicationContext):
        if int(ctx.author.id) != 756509638169460837 and not any(
            role.id
            in [
                staff_manager_role_id,
                community_manager_role_id,
                assistant_director_role_id,
                head_of_operations_role_id,
                developer_role_id,
                owner_role_id,
            ]
            for role in ctx.author.roles
        ):
            await ctx.respond(embed=no_perm_embed, ephemeral=True)
            return
        await ctx.defer(ephemeral=True)
        await ctx.followup.send("Updated!", ephemeral=True)

    @discord.Cog.listener()
    async def on_ready(self):
        pass


def setup(bot):
    bot.add_cog(bss_codes(bot))
