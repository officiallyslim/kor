import os
from datetime import datetime
from discord import option

import discord
import dotenv
import pytz
from discord.commands import Option
from discord.ext import commands, tasks

from commands.fact_commands import fact_group, source_island
from config import bot
from src.facts.get_fact import get_daily_islandfact
from src.global_src.global_channel_id import (
    daily_fact_channel_id,
    daily_fact_log_channel_id,
    general_log_channel_id,
    mod_channel_id,
)
from src.global_src.global_embed import (
    failed_fetch_daily_channel,
    no_perm_embed,
    soon_embed,
)
from src.global_src.global_path import (
    daily_count_path,
)
from src.global_src.global_roles import (
    assistant_director_role_id,
    community_manager_role_id,
    developer_role_id,
    head_of_operations_role_id,
    mr_boomsteak_role_id,
    staff_manager_role_id,
)

dotenv.load_dotenv()
token = str(os.getenv("GITHUB_TOKEN"))


class fact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="change_fact_number", description="Change the daily fact number"
    )
    async def change_fact_number(
        self,
        ctx: discord.ApplicationContext,
        number: Option(int, "The next say fact number"),
    ):  # type: ignore
        if int(ctx.author.id) != 756509638169460837 and not any(
            role.id
            in [
                staff_manager_role_id,
                community_manager_role_id,
                assistant_director_role_id,
                head_of_operations_role_id,
                developer_role_id,
                mr_boomsteak_role_id,
            ]
            for role in ctx.author.roles
        ):
            await ctx.respond(embed=no_perm_embed, ephemeral=True)
            return

        if not float(number).is_integer():
            await ctx.respond(
                "Please enter an integer without decimals!", ephemeral=True
            )
            return

        f = open(daily_count_path, "w")
        f.write(f"{number}")
        f.close()

        await ctx.respond(
            f"The next daily count number set to `{number}`", ephemeral=True
        )

        daily_log_channel = bot.get_channel(daily_fact_log_channel_id)
        general_kor_log_channel = bot.get_channel(general_log_channel_id)

        if daily_log_channel:
            embed = discord.Embed(
                title="Updated daily count",
                description=f"{ctx.author.mention} (`{ctx.author.id}`) updated the daily count to `{number}`",
                colour=discord.Colour(int("51d1f6", 16)),
            )
            await daily_log_channel.send(embed=embed)
        else:
            await general_kor_log_channel.send(embed=failed_fetch_daily_channel)

    @discord.slash_command(
        name="add_custom_island_fact", description="Add new island fact to database"
    )
    @option("fact", description="Fact about Islands (Roblox)")
    @option("img_link", description="Related image of the fact", default=None)
    @option("source_link", description="Source link of the fact", default=None)
    async def add_custom_island_fact(
        self,
        ctx: discord.ApplicationContext,
    ):
        if int(ctx.author.id) != 756509638169460837 and not any(
            role.id
            in [
                staff_manager_role_id,
                community_manager_role_id,
                assistant_director_role_id,
                head_of_operations_role_id,
                developer_role_id,
                mr_boomsteak_role_id,
            ]
            for role in ctx.author.roles
        ):
            await ctx.respond(embed=no_perm_embed, ephemeral=True)
            return

        await ctx.respond(embed=soon_embed, ephemeral=True)

    @discord.Cog.listener()
    async def on_ready(self):
        dailyfact.start()

    print("Loading fact commands...")
    bot.add_application_command(fact_group)
    print("Fact commands loaded!")


def setup(bot):
    bot.add_cog(fact(bot))


# DAILY RANDOM FACT HERE
async def get_fact_number():
    with open(daily_count_path, "r") as f:
        content = f.read()
        number = int(content)
        return number


async def increment_fact_number():
    with open(daily_count_path, "r") as f:
        content = f.read()
        number = int(content)

    number += 1

    with open(daily_count_path, "w") as f:
        f.write(str(number))


fact_sent = False


@tasks.loop(seconds=1)
async def dailyfact():
    global fact_sent
    now = datetime.now(pytz.utc)
    cest = pytz.timezone("Europe/Madrid")

    # Check time
    if (
        now.astimezone(cest).hour == 17
        and now.astimezone(cest).minute == 00
        and not fact_sent
    ):
        channel = bot.get_channel(daily_fact_channel_id)
        fact = await get_daily_islandfact()
        mod_channel = bot.get_channel(mod_channel_id)

        if fact:
            randomislandfact_embed = discord.Embed(
                title="Did you know? 🏝️",
                description=f"{fact['Fact']}",
                colour=discord.Colour(int("d1e8fa", 16)),
            )

            fact_number = await get_fact_number()

            if fact["Image Link"] is not None:
                randomislandfact_embed.set_image(url=f"{str(fact['Image Link'])}")

            if fact["Source Link"] is None:
                await channel.send(
                    f"## <@&1198106586309201950> Random Fact #{fact_number}\n",
                    embed=randomislandfact_embed,
                )
                print("Send daily fact without button")
            else:
                await channel.send(
                    f"## <@&1198106586309201950> Random Fact #{fact_number}\n",
                    embed=randomislandfact_embed,
                    view=source_island(fact["Source Link"]),
                )
                print("Send daily fact with button")

            await increment_fact_number()
            fact_sent = True

            # Send log
            daily_log_channel = bot.get_channel(daily_fact_log_channel_id)

            embed = discord.Embed(
                title=f"Daily random fact status #{fact_number}",
                description=f"{fact['Fact']}",
                colour=discord.Colour(int("d1e8fa", 16)),
            )

            await daily_log_channel.send(embed=embed)

            if fact["Available Facts"] < 5:
                await mod_channel.send(
                    f"<@756509638169460837> There's only **{fact['Available Facts']}** daily facts left!"
                )
        else:
            await mod_channel.send("<@756509638169460837> Daily Fact Error.")

    if now.astimezone(cest).hour == 0 and now.astimezone(cest).minute == 0:
        fact_sent = False
