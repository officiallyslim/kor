import asyncio
import re
from datetime import datetime

import discord

from config import bot
from src.global_src.embed_to_dict import embed_to_dict
from src.global_src.global_channel_id import pixel_art_queue_channel_id
from src.global_src.global_embed import claimed_ticket_embed, no_perm_embed
from src.global_src.global_roles import (
    assistant_director_role_id,
    community_manager_role_id,
    developer_role_id,
    head_administration_role_id,
    head_of_operations_role_id,
    junior_administration_role_id,
    mr_boomsteak_role_id,
    mr_boomsteaks_controller_role_id,
    official_administration_role_id,
    pixel_art_role_id,
    senior_administration_role_id,
    staff_manager_role_id,
    trial_administration_role_id,
)
from src.ticket.utils.pixel_art_utils.db_utils.edit_db_pixel_art import (
    edit_db_pixel_art,
)
from src.ticket.utils.pixel_art_utils.db_utils.get_db_data_pixel_art import (
    check_claimed_pixeL_art_ticket,
    get_pixel_art_channel_id,
    get_queue_message_id,
    get_log_message_id
)
from src.ticket.utils.transcript_website import get_transcript
from src.global_src.global_channel_id import ticket_log_channel_id

async def close_ticket(interaction: discord.Interaction, reason):
    # Check if user have allowed roles
    if int(interaction.user.id) != 756509638169460837 and not any(role.id in [
            pixel_art_role_id,
            junior_administration_role_id,
            trial_administration_role_id,
            mr_boomsteaks_controller_role_id,
            official_administration_role_id,
            senior_administration_role_id,
            head_administration_role_id,
            staff_manager_role_id,
            community_manager_role_id,
            assistant_director_role_id,
            head_of_operations_role_id,
            developer_role_id,
            mr_boomsteak_role_id] for role in interaction.user.roles):
        await interaction.response.send_message(embed=no_perm_embed, ephemeral=True)
        return

    # Get ticket ID
    embed = [embed_to_dict(embed) for embed in interaction.message.embeds]
    ticket_id = re.findall(r"Ticket ID: (\w+)", embed[0]['footer']['text'])[0]

    # Check if user is in claimed user for close
    claim_user_id = check_claimed_pixeL_art_ticket(ticket_id)
    if claim_user_id is not None:
        if interaction.user.id != claim_user_id:
            await interaction.response.send_message(embed=claimed_ticket_embed, ephemeral=True)
            return

    # Gen transcript
    await interaction.response.send_message("🔒Closing ticket...\n\n🔄 Creating transcript... This may take a while!", ephemeral=True)
    channel_id = get_pixel_art_channel_id(ticket_id)
    ticket_channel = bot.get_channel(channel_id)
    status = await get_transcript(ticket_channel, ticket_id)

    if status == "Failed":
        await interaction.edit_original_response(content="🔒**Closing ticket...**\n\n🔄 **Creating transcript...** This may take a while!\n\n❌ Failed generating transcript! Please, report to admins with the ticket id")
        return

    await interaction.edit_original_response(content=f"🔒**Closing ticket...**\n\n🔄 **Creating transcript...** This may take a while!\n\n✅ [Transcript]({status}) generated correctly! Deleting channel in 5 seconds.")
    await asyncio.sleep(5)

    close_time = int(datetime.now().timestamp())
    edit_db_pixel_art(ticket_id=ticket_id, close_time=close_time, close_user_id=interaction.user.id, close_reason=reason)

    print(channel_id)
    print(ticket_channel)
    await ticket_channel.delete(reason=f"Ticket {ticket_id} finished.")

    queue_message_id = get_queue_message_id(ticket_id)
    if queue_message_id is not None:
        queue_message = await bot.get_channel(pixel_art_queue_channel_id).fetch_message(queue_message_id)
        await queue_message.delete(reason="Ticketd clsoed")
        print(f"Ticket {ticket_id} closed")
    else:
        print(f"Ticket {ticket_id} closed")

    log_msg_id = get_log_message_id(ticket_id)
    log_msg = bot.get_channel(ticket_log_channel_id).fetch_message(log_msg_id)
    embed = discord.Embed(
        title=f"Ticket {ticket_id} closed",
        description="",
        color=0x85B3FA
    )
    embed.add_field(name="🕐 Close time", value=f"<t:{close_time}>", inline=False)
    embed.add_field(name="✏️ Close reason",value=f"```{reason}```",inline=False,)
    embed.set_footer(text=f"Ticket ID: {ticket_id}")
    await log_msg.reply(embed=embed)