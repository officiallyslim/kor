import discord
from discord.ext import commands
from src.loa_request.data.roles_hierarchy import builder_roles_hierarchy

class loa_request(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.slash_command(name="max_builder_test", description="Test the welcome feature with specific member")
    async def test_welcome(self, ctx: discord.ApplicationContext):
        await ctx.defer(ephemeral=True)

        author_roles = ctx.author.roles

        levels = [builder_roles_hierarchy.get(role.id, {}).get("level", 0) for role in author_roles]

        max_level = max(levels, default=None)

        if max_level is not None:
            rol_mas_alto = next((role for role in author_roles if builder_roles_hierarchy.get(role.id, {}).get("level") == max_level), None)
            if rol_mas_alto:
                await ctx.respond(f"Max rol: {rol_mas_alto.mention} (level {max_level}).", ephemeral=True)
            else:
                await ctx.respond("Bigger role not found", ephemeral=True)
        else:
            await ctx.respond("No builder roles found", ephemeral=True)


def setup(bot):
    bot.add_cog(loa_request(bot))
