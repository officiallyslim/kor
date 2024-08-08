import discord
from discord.ext import commands
from config import guild_id


class feedback(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="send_ticket_feedback",
        description="Send the ticket feedback for all builders",
    )
    async def send_ticket_feedback_callback(self, ctx: discord.ApplicationContext):
        await ctx.defer(ephemeral=True)

        role_id = 1229570230611742771

        guild = self.bot.get_guild(guild_id)
        if guild is None:
            await ctx.respond("Guild not found.", ephemeral=True)
            return

        role = guild.get_role(role_id)
        if role is None:
            await ctx.respond("Role not found.", ephemeral=True)
            return

        users_with_role = [member for member in guild.members if role in member.roles]

        await ctx.respond(
            f"Found {len(users_with_role)} users with the role.", ephemeral=True
        )

        i = 0

        for member in users_with_role:
            print(member.id)
            print(f"{i+1}/{len(users_with_role)}")
            dm_channel = await member.create_dm()
            feedback_embed = discord.Embed(
                title="You have been invited!",
                description=f"You've been invited to participate in a volunteer survey about the KOR bot ticket system. Your feedback is invaluable in helping us enhance our system and provide you with even better service. We greatly appreciate your time and input!\n\nYou Discord ID is `{member.id}`",
                colour=discord.Colour(int("6692d7", 16)),
            )
            await dm_channel.send(embed=feedback_embed, view=feedback_view())
            i += 1

class feedback_view(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(
            discord.ui.Button(
                label="Lets go!", url="https://forms.gle/KzezQpp41DDBVmYAA"
            )
        )


def setup(bot):
    bot.add_cog(feedback(bot))
