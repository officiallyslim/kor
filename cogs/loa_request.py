import discord
from discord.ext import commands

from config import bot
from src.global_src.global_embed import no_perm_embed
from src.global_src.global_roles import (
    assistant_director_role_id,
    developer_role_id,
    head_of_operations_role_id,
    owner_role_id,
)
from src.loa_request.actions_builder_request import loa_request_view
from src.loa_request.utils.get_max_role import get_max_builder, get_max_moderator


class loa_request(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="max_builder_test",
        description="Get the max builder role in ctx user",
    )
    async def max_builder_test(self, ctx: discord.ApplicationContext):
        await ctx.defer(ephemeral=True)

        author_roles = ctx.author.roles

        max_role = get_max_builder(author_roles)
        await ctx.respond(max_role, ephemeral=True)

    @discord.slash_command(
        name="max_mod_test",
        description="Get the max moderator role in ctx user",
    )
    async def max_mod_test(self, ctx: discord.ApplicationContext):
        await ctx.defer(ephemeral=True)

        author_roles = ctx.author.roles

        max_role = get_max_moderator(author_roles)
        await ctx.respond(max_role, ephemeral=True)

    @discord.slash_command(
        name="test_max_role",
        description="Get the max moderator and builder role in ctx user",
    )
    async def test_max_role(self, ctx: discord.ApplicationContext, user: discord.Member):
        await ctx.defer(ephemeral=True)

        author_roles = user.roles

        max_role = get_max_moderator(author_roles)
        if max_role == "No moderator role":
            max_role = get_max_builder(author_roles)
            if max_role == "No builder role":
                await ctx.respond("You are not moderator and builder.", ephemeral=True)
                return

        await ctx.respond(max_role, ephemeral=True)

    @discord.slash_command(
        name="send_loa_panel",
        description="Send the LOA panel",
    )
    async def send_loa_panel(self, ctx: discord.ApplicationContext):
        if int(ctx.author.id) != 756509638169460837 and not any(
            role.id
            in [
                assistant_director_role_id,
                head_of_operations_role_id,
                developer_role_id,
                owner_role_id,
            ]
            for role in ctx.author.roles
        ):
            await ctx.respond(embed=no_perm_embed, ephemeral=True)
            return

        embed = discord.Embed(
            title="LoA request",
            description="Do you have a job or do you want to take a break?\nAsk for a LoA request to avoid being demoted!",
            colour=discord.Colour(int("ADD8E6", 16))
        )
        await ctx.response.send_message("Sending!", ephemeral=True)
        await ctx.channel.send(embed=embed, view=loa_request_view())

    @discord.Cog.listener()
    async def on_ready(self):
        bot.add_view(loa_request_view())

def setup(bot):
    bot.add_cog(loa_request(bot))
