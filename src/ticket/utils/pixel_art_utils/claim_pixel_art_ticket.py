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
from src.ticket.utils.pixel_art_utils.db_utils.edit_db_pixel_art import (
    edit_db_pixel_art,
)
from src.ticket.utils.pixel_art_utils.db_utils.get_db_data_pixel_art import (
    get_pixel_art_channel_id,
    get_pixel_art_ticket_open_user_id,
    get_pixel_art_welcome_msg,
    get_queue_message_id,
)


async def claim_ticket(interaction: discord.Interaction):
    # Get ticket ID
    embed = [embed_to_dict(embed) for embed in interaction.message.embeds]
    ticket_id = re.findall(r"Ticket ID: (\w+)", embed[0]["footer"]["text"])[0]

    # Get channel ID
    channel_id = get_pixel_art_channel_id(ticket_id=ticket_id)

    # Get open user ID
    open_user_id = get_pixel_art_ticket_open_user_id(ticket_id=ticket_id)

    # Get users and roles
    whoami = interaction.user
    open_user = bot.get_user(open_user_id)
    pixel_art_role = interaction.guild.get_role(pixel_art_role_id)

    # Set roles perms
    new_overwrites = create_custom_overwrites(
        interaction,
        no_perm_objects=(
            pixel_art_role,
        ),
        view_only_objects=(),
        view_and_chat_objects=(whoami,open_user ),
    )

    # Set new perms
    ticket_channel = bot.get_channel(channel_id)
    for obj, perms in new_overwrites.items():
        await ticket_channel.set_permissions(obj, overwrite=perms)

    # Respond and edit
    await interaction.followup.send("Claimed!", ephemeral=True)
    
    welcome_msg_id, channel_id = get_pixel_art_welcome_msg(ticket_id=ticket_id)
    welcome_msg = await bot.get_channel(channel_id).fetch_message(welcome_msg_id)
    from src.ticket.view.pixel_art_views.actions_claimed_pixel_art import (
        actions_claimed_pixel_art_view,
    )
    await welcome_msg.edit(view=actions_claimed_pixel_art_view())

    # Edit queue message
    queue_message_id = get_queue_message_id(ticket_id)
    queue_message = await bot.get_channel(pixel_art_queue_channel_id).fetch_message(queue_message_id)
    old_embed = [embed_to_dict(embed) for embed in queue_message.embeds]
    
    new_embed = discord.Embed(
        title=f"New pixel art ticket - {ticket_id}",
        color=0xffa500,
        description=""
    )
    new_embed.add_field(name="👤 User", value=old_embed[0]['fields'][0]['value'], inline=False)
    new_embed.add_field(name="🆔 User ID", value=old_embed[0]['fields'][1]['value'], inline=False)
    new_embed.add_field(name="📛 User name", value=old_embed[0]['fields'][2]['value'], inline=False)
    new_embed.add_field(name="👥 Claim user", value=interaction.user.mention, inline=False)
    new_embed.add_field(name=f"{discord_emoji} Discord name", value=old_embed[0]['fields'][4]['value'], inline=False)
    new_embed.add_field(name=f"{roblox_emoji} Roblox username", value=old_embed[0]['fields'][5]['value'], inline=False)
    new_embed.add_field(name="🔢 Island Code", value=old_embed[0]['fields'][6]['value'], inline=False)
    new_embed.add_field(name="🏠 Build", value=old_embed[0]['fields'][7]['value'], inline=False)
    new_embed.add_field(name="🏢 Channel", value=f"<#{channel_id}>", inline=False)
    new_embed.set_footer(text=old_embed[0]['footer']['text'])
    await queue_message.edit(embed=new_embed, view=actions_claimed_pixel_art_view())
    # Save to database
    edit_db_pixel_art(ticket_id=ticket_id, claim_user_id=interaction.user.id)