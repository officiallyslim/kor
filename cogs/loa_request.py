import discord
from discord.ext import commands
from src.loa_request.data.roles_hierarchy import (
    builder_roles_hierarchy,
    moderator_roles_hierarchy,
)


def get_max_builder(auhor_roles):
    levels = [
        builder_roles_hierarchy.get(role.id, {}).get("level", 0) for role in auhor_roles
    ]

    max_level = max(levels, default=None)

    if max_level is not None:
        max_role = next(
            (
                role
                for role in auhor_roles
                if builder_roles_hierarchy.get(role.id, {}).get("level") == max_level
            ),
            None,
        )
        if max_role:
            return max_role
        else:
            return "No builder role"
    else:
        return "No builder role"


def get_max_moderator(auhor_roles):
    levels = [
        moderator_roles_hierarchy.get(role.id, {}).get("level", 0)
        for role in auhor_roles
    ]

    max_level = max(levels, default=None)

    if max_level is not None:
        max_role = next(
            (
                role
                for role in auhor_roles
                if moderator_roles_hierarchy.get(role.id, {}).get("level") == max_level
            ),
            None,
        )
        if max_role:
            return max_role
        else:
            return "No moderator role"
    else:
        return "No moderator role"


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


def setup(bot):
    bot.add_cog(loa_request(bot))
