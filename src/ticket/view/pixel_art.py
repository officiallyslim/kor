import json
from datetime import datetime

import discord

from src.global_src.global_embed import error_embed
from src.global_src.global_emojis import smile_pixel_emoji
from src.global_src.global_path import (
    pixel_art_welcome_embed_path,
    ticket_success_embed_path,
    pixel_art_dm_embed_path
)
from src.ticket.utils.db_utils.add_db_pixel_art import add_db_pixel_art
from src.ticket.utils.create_overwrites import create_overwrites
from src.ticket.utils.gen_ticket_key import gen_key
from src.ticket.view.form_pixel_art import form_pixel_art_view
from src.ticket.view.jump_channel import jump_channel
from config import guild_id

mod_role_id = 1222579667207192626
category_id = 1222316215884582924
general_log = 1222664107338240171

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
        await interaction.response.defer(ephemeral=True)

        # Gen ticket id
        ticket_id = gen_key(15)
        print(f"Creating new ticket: {ticket_id}")

        # Get users and roles
        whoami = interaction.user
        mod_role = interaction.guild.get_role(mod_role_id)
        objects = (whoami, mod_role)

        # Set roles perms
        overwrites = create_overwrites(interaction, *objects)

        # Get time
        open_time = int(datetime.now().timestamp())

        # Create ticket
        try:
            new_channel = await interaction.guild.create_text_channel(
                name=f"{interaction.user.name} - pixel",
                overwrites=overwrites,
                topic=f"Ticket ID: {ticket_id}",
                reason="New channel for Pixel Art Builder request",
                category=discord.Object(id=category_id),
            )
        except Exception as e:
            await interaction.response.send_message(error_embed, ephemeral=True)
            print(f"Error when creating channel: {e}")
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
                f"{interaction.user.mention}", embed=embed, view=jump_channel(guild_id, channel_id)
            )
        except discord.Forbidden:
            print(f"Failed send DM to {interaction.user.name}")


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
            queue_msg_id=None,
            log_msg_id=None,
            transcript_thread_id = None,
            claim_status=0,
            claim_user_id=None,
            close_user_id=None,
            close_time=None,
            close_reason=None,
        )
