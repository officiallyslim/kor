import json
from datetime import datetime
from src.ticket.modal.form_builder_request import form_pixel_art_modal

import discord

from config import bot, guild_id
from src.global_src.global_channel_id import ticket_log_channel_id
from src.global_src.global_embed import error_embed, ticket_ban_embed
from src.global_src.global_emojis import smile_pixel_emoji
from src.global_src.global_path import (
    pixel_art_dm_embed_path,
    pixel_art_welcome_embed_path,
    ticket_banned_path,
    ticket_success_embed_path,
    ticket_cooldown_path
)
from src.global_src.global_roles import (
    pixel_art_role_id,
)
from src.ticket.utils.create_overwrites import create_custom_overwrites
from src.ticket.utils.gen_ticket_key import gen_key
from src.ticket.utils.builder_request_utils.db_utils.add_db_builder_request import add_db_pixel_art
from src.ticket.utils.builder_request_utils.db_utils.get_db_data_builder_request import (
    check_open_pixel_art_ticket,
)
from src.ticket.view.jump_channel import jump_channel
from src.ticket.view.builder_request_views.form_builder_request import form_pixel_art_view

class pixel_art_panel_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Pixel Art",
        style=discord.ButtonStyle.primary,
        emoji=smile_pixel_emoji,
        custom_id="pixel_art_panel_button",
    )
    async def pixel_art_panel_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Get time
        open_time = int(datetime.now().timestamp())

        # Check if user is banned from tickets
        with open(ticket_banned_path, 'r') as f:
            data = json.load(f)

        if str(interaction.user.id) in data:
            await interaction.response.send_message(embed=ticket_ban_embed, ephemeral=True)
            return

        # Check if is in cooldown
        with open(ticket_cooldown_path, 'r') as f:
            data = json.load(f)
            last_time = data.get(str(interaction.user.id), "Not found")

        if last_time == "Not found":
            data[str(interaction.user.id)] = open_time
            with open(ticket_cooldown_path, 'w') as f:
                json.dump(data, f, indent=4)
        else:
            timeout_time = last_time + 300
            if open_time < timeout_time:
                await interaction.response.send_message("You're opening tickets so fast! Please wait a moment to open another one.", ephemeral=True)
                return
            else:
                data[str(interaction.user.id)] = open_time
                with open(ticket_cooldown_path, 'w') as f:
                    json.dump(data, f, indent=4)

        # Check user have current open channel
        open_ticket = check_open_pixel_art_ticket(int(interaction.user.id))
        if open_ticket is not False:  # compare with False, not the function
            ticket_id, channel_id = open_ticket
            embed = discord.Embed(
                title="You already have an open pixel art ticket!",
                description=f"You have the pixel art ticket: `{ticket_id}` already opened.\nYou can enter by clicking the button below.",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, view=jump_channel(guild_id, channel_id), ephemeral=True)
            return

        # Defer response
        modal = form_pixel_art_modal(title="Pixel Art Form",name=interaction.user.name, status="new")
        await interaction.response.send_modal(modal)

        # Gen ticket id
        ticket_id = gen_key(15)
        print(f"Creating new ticket: {ticket_id}")

        # Get users and roles
        whoami = interaction.user
        pixel_art_role = interaction.guild.get_role(pixel_art_role_id)

        # Set roles perms
        overwrites = create_custom_overwrites(
            interaction,
            no_perm_objects=(),
            view_only_objects=(whoami,),
            view_and_chat_objects=(
                pixel_art_role,
            ),
        )

        # Create ticket
        try:
            new_channel = await interaction.guild.create_text_channel(
                name=f"{interaction.user.name} - pixel",
                overwrites=overwrites,
                topic=f"Ticket ID: {ticket_id}",
                reason="New channel for Pixel Art Builder request",
                category=discord.Object(id=1223274346429288480),
            )
        except Exception as e:
            await interaction.followup.send(embed=error_embed, ephemeral=True)
            print(f"Error when creating channel: {e}")
            import traceback
            traceback.print_exc()
            return

        # Send welcome message
        with open(pixel_art_welcome_embed_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        embed_info = data["embeds"][0]
        embed_info["title"] = embed_info["title"].replace("[USER]", interaction.user.name)
        embed_info["footer"]["text"] = embed_info["footer"]["text"].replace("[KEY]", ticket_id)
        embed = discord.Embed.from_dict(embed_info)

        welcome_message = await new_channel.send(
            f"{interaction.user.mention}", embed=embed, view=form_pixel_art_view()
        )

        # Respond the message
        with open(ticket_success_embed_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for embed_info in data["embeds"]:
            embed = discord.Embed.from_dict(embed_info)

        channel_id = new_channel.id
        await interaction.followup.send(
            embed=embed, view=jump_channel(guild_id, channel_id), ephemeral=True
        )

        # Send DM
        try:    
            dm = await interaction.user.create_dm()
            with open(pixel_art_dm_embed_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            embed_info = data["embeds"][0]
            embed_info["footer"]["text"] = embed_info["footer"]["text"].replace("[KEY]", ticket_id)
            embed = discord.Embed.from_dict(embed_info)

            dm_message = await dm.send(
                content="", embed=embed, view=jump_channel(guild_id, channel_id)
            )
        except discord.Forbidden:
            print(f"Failed send DM to {interaction.user.name}")

        # Send to log
        embed = discord.Embed(
            title="New Pixel Art ticket registered",
            description="Ticket details:",
            color=0xff8000,
        )
        embed.add_field(name="👤 User", value=interaction.user.mention, inline=False)
        embed.add_field(name="🆔 User ID", value=f"`{interaction.user.id}`", inline=False)
        embed.add_field(name="📛 User name", value=interaction.user.name, inline=False)
        embed.add_field(name="📅 Joined", value=f"<t:{int(interaction.user.joined_at.timestamp())}:R>", inline=False)
        embed.add_field(name="👥 Claim user", value="`No claimed`", inline=False)
        embed.add_field(name="📑 Open reason", value="```Request a Pixel Art Builder```", inline=False)
        embed.add_field(name="🕒 Open time", value=f"<t:{open_time}>", inline=False)
        embed.add_field(name="🏢 Ticket Channel", value=f"<#{channel_id}>", inline=False)
        embed.set_footer(text=f"Ticket ID: {ticket_id}")

        log_channel = bot.get_channel(ticket_log_channel_id)
        log_message = await log_channel.send(embed=embed)

        # Add data to database
        add_db_pixel_art(
            ticket_id=ticket_id,
            open_user_id=interaction.user.id,
            open_time=open_time,
            open_reason="Request A Pixel Art Builder",
            form_name=None,
            form_roblox_user=None,
            form_island_code=None,
            form_build=None,
            form_build_desp=None,
            form_build_img=None,
            channel_id=channel_id,
            welcome_msg_id=welcome_message.id,
            dm_msg_id=dm_message.id,
            confirm_message_id=None,
            queue_msg_id=None,
            log_msg_id=log_message.id,
            transcript_key = None,
            claim_user_id=None,
            close_user_id=None,
            close_time=None,
            close_reason=None,
        )