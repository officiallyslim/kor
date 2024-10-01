import asyncio
import re
from datetime import datetime

import discord

from config import bot
from src.global_src.global_channel_id import (
    ticket_log_channel_id,
)
from src.global_src.global_embed import claimed_ticket_embed, error_embed, no_perm_embed
from src.global_src.global_roles import (
    pixel_art_role_id,
    expo_role_id,
    shop_role_id,
    industrial_role_id,
    farm_role_id,
    structure_role_id,
    recruitment_role_id,
    support_role_id,
    giveaway_role_id,
)
from src.ticket.utils.builder_request_utils.builder_ticket_type import ticket_type_dict
from src.ticket.utils.builder_request_utils.db_utils.edit_db_builder_request import (
    edit_builder_request_db,
)
from src.ticket.utils.builder_request_utils.db_utils.get_db_data_builder_request import (
    check_claimed_builder_ticket,
    get_builder_channel_id,
    get_builder_dm_message_id,
    get_builder_log_message_id,
    get_builder_queue_message_id,
    get_builder_ticket_type,
)
from src.ticket.utils.transcript_website import get_transcript
from src.global_src.global_path import ticket_saved_password_path

async def close_ticket(interaction: discord.Interaction, reason, ticket_id, password):
    # Check if user have allowed roles
    if int(interaction.user.id) != 756509638169460837 and not any(
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
        for role in interaction.user.roles
    ):
        await interaction.response.send_message(embed=no_perm_embed, ephemeral=True)
        return

    # Get ticket ID
    if ticket_id is None:
        try:
            match = re.findall(r"Ticket ID: (\w+)", interaction.channel.topic)
            if match:
                ticket_id = match[0]
            else:
                await interaction.response.send_message(
                    embed=error_embed, ephemeral=True
                )
                return
        except Exception:
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return

    # Get ticket type
    ticket_type = get_builder_ticket_type(ticket_id=ticket_id)
    for key, value in ticket_type_dict.items():
        if value["type"] == ticket_type:
            queue_channel_id = value["queue_channel_id"]

    # Check if user is in claimed user for close or is the owner or correct password
    saved_password_file = open(ticket_saved_password_path, "r")
    saved_password = saved_password_file.read()
    saved_password_file.close()

    claim_user_id = check_claimed_builder_ticket(ticket_id)
    if claim_user_id is not None:
        if (interaction.user.id != claim_user_id and 
            interaction.user.id != 731894309615304815 and 
            password != saved_password):

            # Password no provided
            if password is None and interaction.user.id != 731894309615304815:
                await interaction.response.send_message(
                    content=f"Claimed by <@{claim_user_id}> ({claim_user_id}).",
                    embed=claimed_ticket_embed, ephemeral=True
                )
                return
            # If the password is incorrect
            if password != saved_password:
                await interaction.response.send_message(
                    content=f"Claimed by <@{claim_user_id}> ({claim_user_id}). Incorrect password.",
                    embed=claimed_ticket_embed, ephemeral=True
                )
                return


    # Gen transcript
    await interaction.response.send_message(content="Closing...", ephemeral=True)
    status_message = await interaction.channel.send(
        "🔒Closing ticket...\n\n🔄 Creating transcript... This may take a while!"
    )
    channel_id = get_builder_channel_id(ticket_id)
    ticket_channel = bot.get_channel(channel_id)

    try:
        status = await get_transcript(ticket_channel, ticket_id)

        if status[0] == "Failed":
            await status_message.edit(
                content="🔒**Closing ticket...**\n\n🔄 **Creating transcript...** This may take a while!\n\n❌ Failed generating transcript! Please, report to admins with the ticket id"
            )
            return

        await status_message.edit(
            content=f"🔒**Closing ticket...**\n\n🔄 **Creating transcript...** This may take a while!\n\n✅ [Transcript]({status[0]}) generated correctly! Deleting channel in 5 seconds."
        )
        await asyncio.sleep(5)

    except Exception as e:
        await status_message.edit(
            content=f"🔒**Closing ticket...**\n\n🔄 **Creating transcript...** This may take a while!\n\n❌ Something failed genereting transcript.\nError: ```{e}```**\nPlease, report to <@756509638169460837>.**"
        )
        return

    close_time = int(datetime.now().timestamp())
    edit_builder_request_db(
        ticket_id=ticket_id,
        close_time=close_time,
        close_user_id=interaction.user.id,
        close_reason=reason,
        transcript_key=status[1],
    )

    await ticket_channel.delete(reason=f"Ticket {ticket_id} finished.")

    queue_message_id = get_builder_queue_message_id(ticket_id)
    if queue_message_id is not None:
        queue_message = await bot.get_channel(queue_channel_id).fetch_message(
            queue_message_id
        )  # e
        await queue_message.delete(reason="Ticketd clsoed")
        print(f"Ticket {ticket_id} closed")
    else:
        print(f"Ticket {ticket_id} closed")

    log_msg_id = get_builder_log_message_id(ticket_id)
    log_message = await bot.get_channel(ticket_log_channel_id).fetch_message(log_msg_id)

    open_user_data = get_builder_dm_message_id(ticket_id)
    if open_user_data[1] is not None:
        open_user = bot.get_user(open_user_data[0])
        try:
            dm_channel = open_user.dm_channel
            if dm_channel is None:
                dm_channel = await open_user.create_dm()
            dm_message = await dm_channel.fetch_message(open_user_data[1])
            await dm_message.edit(view=None)
            embed = discord.Embed(
                title="Thank you for contacting us!",
                description=f"Your ticket `{ticket_id}` has been closed by one of our staff members with the following reason: ```{reason}```",
                color=0x28A745,
            )
            embed.set_footer(text=f"Ticket ID: {ticket_id}")
            await dm_message.reply(embed=embed)
        except Exception:
            pass
    else:
        print(f"{open_user} dm is probably is closed xd?")

    embed = discord.Embed(
        title=f"Ticket {ticket_id} closed", description="", color=0x5cb85c
    )
    embed.add_field(name="🕐 Close time", value=f"<t:{close_time}>", inline=False)
    embed.add_field(
        name="🙍 Close user",
        value=f"{interaction.user.mention} - {interaction.user.id}",
        inline=False,
    )
    embed.add_field(
        name="✏️ Close reason",
        value=f"```{reason}```",
        inline=False,
    )
    embed.add_field(
        name="🗝️ Web transcript key",
        value=f"```{status[1]}```",
        inline=False,
    )
    embed.add_field(
        name="🌐 Web Transcript",
        value=f"[Open in browser]({status[0]})",
        inline=False,
    )
    embed.set_footer(text=f"Ticket ID: {ticket_id}")
    await log_message.reply(embed=embed)