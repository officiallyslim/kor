from discord.ext import commands


class loa_request(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    pass


def setup(bot):
    bot.add_cog(loa_request(bot))
