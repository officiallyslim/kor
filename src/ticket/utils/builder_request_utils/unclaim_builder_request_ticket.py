import re

import discord

from config import bot
from src.global_src.embed_to_dict import embed_to_dict
from src.global_src.global_channel_id import pixel_art_queue_channel_id
from src.global_src.global_emojis import discord_emoji, roblox_emoji
from src.global_src.global_roles import (
    pixel_art_role_id,
)
from src.ticket.utils.create_overwrites import create_custom_overwrites
from src.ticket.utils.builder_request_utils.db_utils.edit_db_builder_request import (
    edit_builder_request_db,
)
from src.ticket.utils.builder_request_utils.db_utils.get_db_data_builder_request import (
    get_builder_channel_id,
    get_builder_open_user_id,
    get_builder_welcome_msg,
    get_builder_queue_message_id,
)


async def unclaim_ticket(interaction: discord.Interaction):
    # Get ticket ID
    embed = [embed_to_dict(embed) for embed in interaction.message.embeds]
    ticket_id = re.findall(r"Ticket ID: (\w+)", embed[0]["footer"]["text"])[0]

    # Get channel ID
    channel_id = get_builder_channel_id(ticket_id=ticket_id)

    # Get open user ID
    open_user_id = get_builder_open_user_id(ticket_id=ticket_id)

    # Get users and roles
    whoami = interaction.user
    open_user = bot.get_user(open_user_id)
    pixel_art_role = interaction.guild.get_role(pixel_art_role_id)

    # Set roles perms
    new_overwrites = create_custom_overwrites(
        interaction,
        no_perm_objects=(),
        view_only_objects=(),
        view_and_chat_objects=(
            whoami,
            open_user,
            pixel_art_role,
        ),
    )

    # Set new perms
    ticket_channel = bot.get_channel(channel_id)
    for obj, perms in new_overwrites.items():
        await ticket_channel.set_permissions(obj, overwrite=perms)

    # Respond and edit
    await interaction.followup.send("Unclaimed!", ephemeral=True)

    welcome_msg_id, channel_id = get_builder_welcome_msg(ticket_id=ticket_id)
    welcome_msg = await bot.get_channel(channel_id).fetch_message(welcome_msg_id)
    from src.ticket.view.builder_request_views.actions_builder_request import actions_pixel_art_view
    await welcome_msg.edit(view=actions_pixel_art_view())

    # Edit queue message
    queue_message_id = get_builder_queue_message_id(ticket_id)
    queue_message = await bot.get_channel(pixel_art_queue_channel_id).fetch_message(queue_message_id)
    old_embed = [embed_to_dict(embed) for embed in queue_message.embeds]
    
    new_embed = discord.Embed(
        title=f"Pixel art ticket - {ticket_id}",
        color=0xffa500,
        description=""
    )
    new_embed.add_field(name="👤 User", value=old_embed[0]['fields'][0]['value'], inline=False)
    new_embed.add_field(name="🆔 User ID", value=old_embed[0]['fields'][1]['value'], inline=False)
    new_embed.add_field(name="📛 User name", value=old_embed[0]['fields'][2]['value'], inline=False)
    new_embed.add_field(name="👥 Claim user", value="`No claimed`", inline=False)
    new_embed.add_field(name=f"{discord_emoji} Discord name", value=old_embed[0]['fields'][4]['value'], inline=False)
    new_embed.add_field(name=f"{roblox_emoji} Roblox username", value=old_embed[0]['fields'][5]['value'], inline=False)
    new_embed.add_field(name="🔢 Island Code", value=old_embed[0]['fields'][6]['value'], inline=False)
    new_embed.add_field(name="🏠 Build", value=old_embed[0]['fields'][7]['value'], inline=False)
    new_embed.add_field(name="🏢 Channel", value=f"<#{channel_id}>", inline=False)
    new_embed.set_footer(text=old_embed[0]['footer']['text'])
    await queue_message.edit(embed=new_embed)
    # Save to database
    edit_builder_request_db(ticket_id=ticket_id, claim_user_id=None)