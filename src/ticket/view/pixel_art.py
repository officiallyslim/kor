import json
from datetime import datetime

import discord

from src.global_src.global_embed import error_embed
from src.global_src.global_emojis import smile_pixel_emoji
from src.global_src.global_path import (
    pixel_art_welcome_embed_path,
    ticket_success_embed_path,
)
from src.ticket.utils.add_db.add_db_pixel_art import add_db_pixel_art
from src.ticket.utils.create_overwrites import create_overwrites
from src.ticket.utils.gen_ticket_key import gen_key
from src.ticket.view.form_pixel_art import form_pixel_art_view
from src.ticket.view.jump_channel import jump_channel

mod_role_id = 1222579667207192626
category_id = 1222316215884582924
guild_id = 1222316215884582922

class pixel_art_panel_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Pixel Art", style=discord.ButtonStyle.primary, emoji=smile_pixel_emoji, custom_id="pixel_art_panel_button")
    async def pixel_art_panel_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        ticket_id = gen_key(15) # Gen ticket id
        print(f"Creating new ticket: {ticket_id}")

        whoami = interaction.user
        mod_role = interaction.guild.get_role(mod_role_id)
        objects = (whoami, mod_role)

        # Make roles
        overwrites = create_overwrites(interaction, *objects)

        # Create ticket
        try:
            new_channel = await interaction.guild.create_text_channel(
                name=f"{interaction.user.name} - {ticket_id}",
                overwrites=overwrites,
                topic=f"{interaction.user.name} Pixel Art Builder request\n Created at <t:{int(datetime.now().timestamp())}>",
                reason="New channel for Pixel Art Builder request",
                category=discord.Object(id=category_id)
            )
        except Exception as e:
            await interaction.response.send_message(error_embed, ephemeral=True)
            print(f"Error when creating channel: {e}")
            return

        # Send welcome message
        with open(pixel_art_welcome_embed_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        embed_info = data['embeds'][0]
        embed_info['title'] = embed_info['title'].replace('[user]', interaction.user.name)
        embed_info['description'] = embed_info['description'].replace('[user]', interaction.user.name)
        embed_info['footer']['text'] = embed_info['footer']['text'].replace('[KEY]', ticket_id)
        embed = discord.Embed.from_dict(embed_info)

        await new_channel.send(f"{interaction.user.mention}",embed=embed, view=form_pixel_art_view())

        # Respond the message
        with open(ticket_success_embed_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for embed_info in data['embeds']:
            embed = discord.Embed.from_dict(embed_info)

        channel_id = new_channel.id
        await interaction.followup.send(embed=embed, view=jump_channel(guild_id, channel_id), ephemeral=True)

        # Add data to database
        add_db_pixel_art(
            ticket_id='test2',
            open_user_id=123,
            open_time=1234567890,
            open_reason='Prueba',
            form_name='FormularioTest',
            form_roblox_user='UsuarioRoblox',
            form_island_code='CódigoIsla',
            form_build='Construcción',
            form_build_desp='DescripciónConstrucción',
            form_build_img='ImagenConstrucción',
            channel_id=123456789,
            welcome_msg_id=123456789,
            dm_msg_id=123456789,
            queue_msg_id=123456789,
            log_msg_id=123456789,
            claim_status=1,
            claim_user_id=123456789,
            close_user_id=123456789,
            close_time=1234567890,
            close_reason='RazónCierre'
        )