import discord
from discord.ext import commands
from src.loa_request.data.roles_hierarchy import builder_roles_hierarchy


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
            return "Error"
    else:
        return "No builder"


class loa_request(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="max_builder_test",
        description="Test the welcome feature with specific member",
    )
    async def test_welcome(self, ctx: discord.ApplicationContext):
        await ctx.defer(ephemeral=True)

        author_roles = ctx.author.roles

        max_role = get_max_builder(author_roles)
        await ctx.respond(max_role, ephemeral=True)


def setup(bot):
    bot.add_cog(loa_request(bot))
