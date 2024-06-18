import discord
import re
from src.global_src.global_embed import no_perm_embed
from src.global_src.global_roles import (
    expo_role_id,
    farm_role_id,
    giveaway_role_id,
    industrial_role_id,
    pixel_art_role_id,
    recruitment_role_id,
    shop_role_id,
    structure_role_id,
    support_role_id,
)
from src.ticket.utils.builder_request_utils.db_utils.get_db_data_builder_request import (
    get_all_ticket_info,
)
from src.global_src.global_embed import error_embed


async def view_ticket_info_callback(ctx: discord.ApplicationContext, ticket_id: str):
    if int(ctx.user.id) != 756509638169460837 and not any(
        role.id
        in [
            pixel_art_role_id,
            expo_role_id,
            shop_role_id,
            industrial_role_id,
            farm_role_id,
            structure_role_id,
            recruitment_role_id,
            support_role_id,
            giveaway_role_id,
        ]
        for role in ctx.user.roles
    ):
        await ctx.response.send_message(embed=no_perm_embed, ephemeral=True)
        return

    if ticket_id is None:
        try:
            ticket_id_match = re.findall(r"Ticket ID: (\w+)", ctx.channel.topic)
            ticket_id = ticket_id_match[0]
        except Exception:
            await ctx.response.send_message(
                "Sorry, you need provide the ticket ID or be in the same channel.",
                ephemeral=True,
            )
            return

    try:
        ticket_data = get_all_ticket_info(ticket_id=ticket_id)
        if ticket_data:

            if ticket_data.close_time is not None:
                current_ticket_status = "Ticket is open"
            elif ticket_data.claim_user_id is not None:
                current_ticket_status = (
                    f"Currently claimed by <@{ticket_data.claim_user_id}>"
                )
            else:
                current_ticket_status = "Ticket is closed"

            info_embed = discord.Embed(
                title=f"Ticket {ticket_data.ticket_id} information",
                description=f"""
                **📢 Current status: {current_ticket_status}** 
                **🙍 Open user:** <@{ticket_data.open_user_id}""",
                colour=discord.Colour(int("5cb85c", 16)),
            )
            info_embed.add_field(
                name="TEST",
                value=f"A",
                inline=False,
            )

            await ctx.response.send_message(content=f"```{ticket_data}```")
        else:
            await ctx.response.send_message(content="Ticket data not found")
    except Exception:
        await ctx.response.send_message(embed=error_embed, ephemeral=True)
