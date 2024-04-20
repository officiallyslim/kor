import asyncio
import re
from datetime import datetime

import discord

from config import bot
from src.global_src.global_channel_id import pixel_art_queue_channel_id
from src.global_src.global_embed import claimed_ticket_embed, no_perm_embed, error_embed
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
from src.ticket.utils.builder_request_utils.db_utils.edit_db_builder_request import (
    edit_builder_request_db,
)
from src.ticket.utils.builder_request_utils.db_utils.get_db_data_builder_request import (
    check_claimed_builder_ticket,
    get_builder_channel_id,
    get_builder_queue_message_id,
    get_builder_log_message_id,
    get_builder_dm_message_id
)
from src.ticket.utils.transcript_website import get_transcript
from src.global_src.global_channel_id import ticket_log_channel_id

async def close_ticket(interaction: discord.Interaction, reason, ticket_id):
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
    print(ticket_id)
    if ticket_id is None:
        try:
            print("Trying get ticket id")
            print(interaction.channel.topic)
            match = re.findall(r"Ticket ID: (\w+)", interaction.channel.topic)
            if match:
                ticket_id = match[0]
                print(ticket_id)
            else:
                await interaction.response.send_message(embed=error_embed, ephemeral=True)
                return
        except Exception:
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return

    # Check if user is in claimed user for close
    claim_user_id = check_claimed_builder_ticket(ticket_id)
    if claim_user_id is not None:
        if interaction.user.id != claim_user_id:
            await interaction.response.send_message(embed=claimed_ticket_embed, ephemeral=True)
            return

    # Gen transcript
    status_message = await interaction.response.send_message("🔒Closing ticket...\n\n🔄 Creating transcript... This may take a while!", ephemeral=True)
    channel_id = get_builder_channel_id(ticket_id)
    ticket_channel = bot.get_channel(channel_id)
    status = await get_transcript(ticket_channel, ticket_id)

    if status[0] == "Failed":
        await status_message.edit(content="🔒**Closing ticket...**\n\n🔄 **Creating transcript...** This may take a while!\n\n❌ Failed generating transcript! Please, report to admins with the ticket id")
        return

    await status_message.edit(content=f"🔒**Closing ticket...**\n\n🔄 **Creating transcript...** This may take a while!\n\n✅ [Transcript]({status[0]}) generated correctly! Deleting channel in 5 seconds.")
    await asyncio.sleep(5)

    close_time = int(datetime.now().timestamp())
    edit_builder_request_db(ticket_id=ticket_id, close_time=close_time, close_user_id=interaction.user.id, close_reason=reason, transcript_key=status[1])

    await ticket_channel.delete(reason=f"Ticket {ticket_id} finished.")

    queue_message_id = get_builder_queue_message_id(ticket_id)
    if queue_message_id is not None:
        queue_message = await bot.get_channel(pixel_art_queue_channel_id).fetch_message(queue_message_id)
        await queue_message.delete(reason="Ticketd clsoed")
        print(f"Ticket {ticket_id} closed")
    else:
        print(f"Ticket {ticket_id} closed")

    log_msg_id = get_builder_log_message_id(ticket_id)
    log_message = await bot.get_channel(ticket_log_channel_id).fetch_message(log_msg_id)

    open_user_data = get_builder_dm_message_id(ticket_id)
    if open_user_data is not None:
        open_user = bot.get_user(open_user_data[0])
        dm_channel = open_user.dm_channel
        if dm_channel is None:
            dm_channel = await open_user.create_dm()
        dm_message = await dm_channel.fetch_message(open_user_data[1])
        await dm_message.edit(view=None)
        embed = discord.Embed (
            title="Thank you for contacting us!",
            description=f"Your ticket `{ticket_id}` has been closed by one of our staff members with the following reason: ```{reason}```",
            color=0x28a745
        )
        embed.set_footer(text=f"Ticket ID: {ticket_id}")
        await dm_message.reply(embed=embed)

    embed = discord.Embed(
        title=f"Ticket {ticket_id} closed",
        description="",
        color=0x85B3FA
    )
    embed.add_field(name="🕐 Close time", value=f"<t:{close_time}>", inline=False)
    embed.add_field(name="✏️ Close reason",value=f"```{reason}```",inline=False,)
    embed.add_field(name="🗝️ Web transcript key",value=f"```{status[1]}```",inline=False,)
    embed.add_field(name="🌐 Web Transcript",value=f"[Open in browser]({status[0]})",inline=False,)
    embed.set_footer(text=f"Ticket ID: {ticket_id}")
    await log_message.reply(embed=embed)