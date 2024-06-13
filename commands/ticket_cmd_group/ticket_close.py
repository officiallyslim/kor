
import discord
from discord import option

from commands.ticket_commands import ticket_group
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
from src.ticket.utils.builder_request_utils.close_builder_request_ticket import (
    close_ticket,
)


@ticket_group.command(name="close", description="Close the ticket")
@option("close_reason", description="Close ticket reason")
@option("ticket_id", description="The ID of the ticket you want to close", default=None)
@option("password", description="Close the ticket even if its claimed", default=None)

async def close_ticket_cmd(ctx: discord.ApplicationContext, close_reason: str, ticket_id: str, password:str):
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

    await close_ticket(interaction=ctx, reason=close_reason, ticket_id=ticket_id, password=password)
