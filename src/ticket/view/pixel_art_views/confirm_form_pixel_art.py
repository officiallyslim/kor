import re

import discord

from config import bot
from src.global_src.embed_to_dict import embed_to_dict
from src.global_src.global_embed import no_perm_embed
from src.global_src.global_emojis import send_emoji
from src.global_src.global_roles import pixel_art_role_id
from src.ticket.utils.create_overwrites import create_view_and_chat_overwrites
from src.ticket.utils.pixel_art_utils.db_utils.edit_db_pixel_art import edit_db_pixel_art
from src.ticket.utils.pixel_art_utils.db_utils.get_db_data_pixel_art import (
    get_pixel_art_ticket_open_user_id,
    get_pixel_art_welcome_msg,
    get_log_message_id
)
from src.global_src.global_channel_id import pixel_art_queue_channel_id
from src.ticket.view.pixel_art_views.actions_pixel_art import (
    actions_pixel_art_view,
)
from src.global_src.global_channel_id import ticket_log_channel_id
from src.global_src.global_emojis import roblox_emoji, discord_emoji

class confirm_form_pixel_art_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) 

    @discord.ui.button(label="Send!", style=discord.ButtonStyle.green, emoji=send_emoji, custom_id="send_form_pixel_art_view")
    async def send_form_pixel_art_view(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Get ticket ID
        ticket_id = re.findall(r"Ticket ID: (\w+)", interaction.channel.topic)[0]

        # Verify user
        open_user_id = get_pixel_art_ticket_open_user_id(ticket_id)
        if open_user_id is not None and int(interaction.user.id) != int(open_user_id):
            await interaction.response.send_message(embed=no_perm_embed, ephemeral=True)

        # Get form data
        embed = [embed_to_dict(embed) for embed in interaction.message.embeds]
        name = embed[0]['fields'][0]['value'].replace("```", "")
        roblox_username = embed[0]['fields'][1]['value'].replace("```", "")
        island_code = embed[0]['fields'][2]['value'].replace("```", "")
        build = embed[0]['fields'][3]['value'].replace("```", "")
        edit_db_pixel_art(
            ticket_id=ticket_id,
            form_name=name,
            form_roblox_user=roblox_username,
            form_island_code=island_code,
            form_build=build,
        )

        # Respond and delete self message
        embed = discord.Embed(
            title="Thank you for complete the form!",
            description=f"Please, wait our <@&{pixel_art_role_id}> contact you.\nYou can now send a **image** of the construction that you want!",
            color=0x28a745
        )
        await interaction.response.send_message(content="<@&{pixel_art_role_id}>", embed=embed)
        await interaction.message.delete(reason=f"Deleting form confirm message from the ticket {ticket_id}")

        welcome_msg_id, channel_id = get_pixel_art_welcome_msg(ticket_id)
        welcome_msg = await bot.get_channel(channel_id).fetch_message(welcome_msg_id)

        new_welcome_embed = discord.Embed(
            title=f"Welcome {interaction.user.name}",
            description="Please wait for a member of the staff to contact you.\n\n## Form information",
            color=0x58B9FF
        )
        new_welcome_embed.add_field(name="Discord name", value=f"```{name}```", inline=False)
        new_welcome_embed.add_field(name="Roblox username", value=f"```{roblox_username}```", inline=False)
        new_welcome_embed.add_field(name="Island Code", value=f"```{island_code}```", inline=False)
        new_welcome_embed.add_field(name="Build", value=f"```{build}```", inline=False)
        new_welcome_embed.set_footer(text=f"Ticket ID: {ticket_id}")
        await welcome_msg.edit(content="", embed=new_welcome_embed)

        # Give perm for chat to user
        new_overwrites = create_view_and_chat_overwrites(
            interaction, interaction.user,
        )
        ticket_channel = bot.get_channel(interaction.channel.id)
        await ticket_channel.set_permissions(interaction.user, overwrite=new_overwrites[interaction.user])

        # Advise ticket to mods
        pixel_art_queue_channel = bot.get_channel(pixel_art_queue_channel_id)
        embed = discord.Embed(
            title=f"New pixel art ticket - {ticket_id}",
            color=0xffa500,
            description=""
        )
        embed.add_field(name="👤 User", value=interaction.user.mention, inline=False)
        embed.add_field(name="🆔 User ID", value=f"`{interaction.user.id}`", inline=False)
        embed.add_field(name="📛 User name", value=interaction.user.name, inline=False)
        embed.add_field(name="👥 Claim user", value="`No claimed`", inline=False)
        embed.add_field(name=f"{discord_emoji} Discord name", value=f"```{name}```", inline=False)
        embed.add_field(name=f"{roblox_emoji} Roblox username", value=f"```{roblox_username}```", inline=False)
        embed.add_field(name="🔢 Island Code", value=f"```{island_code}```", inline=False)
        embed.add_field(name="🏠 Build", value=f"```{build}```", inline=False)
        embed.set_footer(text=f"Ticket ID: {ticket_id}")

        # Save queue msg to database
        queue_msg = await pixel_art_queue_channel.send(content="", embed=embed, view=actions_pixel_art_view())
        queue_msg_id = queue_msg.id
        edit_db_pixel_art(ticket_id, queue_msg_id=queue_msg_id)

        # Send to logs
        log_msg_id = get_log_message_id(ticket_id)
        log_message = await bot.get_channel(ticket_log_channel_id).fetch_message(log_msg_id)
        embed = discord.Embed(
            title=f"New form answers in ticket {ticket_id}",
            description="",
            color=0x85b3fa
        )
        embed.add_field(name=f"{discord_emoji} Discord name", value=f"```{name}```", inline=False)
        embed.add_field(name=f"{roblox_emoji} Roblox username", value=f"```{roblox_username}```", inline=False)
        embed.add_field(name="🔢 Island Code", value=f"```{island_code}```", inline=False)
        embed.add_field(name="🏠 Build", value=f"```{build}```", inline=False)
        embed.set_footer(text=f"Ticket ID: {ticket_id}")
        await log_message.reply(embed=embed)

    @discord.ui.button(label="Edit", style=discord.ButtonStyle.gray, emoji="✏️", custom_id="edit_form_pixel_art_view")
    async def edit_form_pixel_art_view(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Get ticket ID
        ticket_id = re.findall(r"Ticket ID: (\w+)", interaction.channel.topic)[0]

        # Verify user
        open_user_id = get_pixel_art_ticket_open_user_id(ticket_id)
        if int(interaction.user.id) != int(open_user_id):
            await interaction.response.send_message(embed=no_perm_embed, ephemeral=True)

        # Get old data
        embed = [embed_to_dict(embed) for embed in interaction.message.embeds]
        name = embed[0]['fields'][0]['value'].replace("```", "")
        roblox_username = embed[0]['fields'][1]['value'].replace("```", "")
        island_code = embed[0]['fields'][2]['value'].replace("```", "")
        build = embed[0]['fields'][3]['value'].replace("```", "")

        # Send modal
        from src.ticket.modal.form_pixel_art import form_pixel_art_modal
        modal = form_pixel_art_modal(title="Pixel Art Form", name=name, status="edit", roblox_user=roblox_username, island_code=island_code, build=build)
        await interaction.response.send_modal(modal)
