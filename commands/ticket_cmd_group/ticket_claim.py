import discord

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
import re
from src.ticket.utils.builder_request_utils.claim_builder_request_ticket import (
    claim_ticket,
)


async def claim_ticket_cmd(ctx: discord.ApplicationContext):
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

    # Get ticket ID
    try:
        ticket_id = re.findall(r"Ticket ID: (\w+)", ctx.channel.topic)
    except Exception:
        ticket_id = None

    if ticket_id is None:
        await ctx.response.send_message(
            "Sorry, you need be in the same ticket channel for claim!",
            ephemeral=True,
        )
        return

    await claim_ticket(
        interaction=ctx, ticket_id={"origin": "button", "ticket_id": ticket_id}
    )
