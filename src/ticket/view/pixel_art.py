import discord
from src.global_src.global_emojis import smile_pixel_emoji
from src.ticket.utils.create_overwrites import create_overwrites
from typing import Union
from src.ticket.utils.gen_ticket_key import gen_key
from datetime import datetime
import json
from src.global_src.global_path import pixel_art_welcome_embed_path, ticket_success_embed_path
from src.global_src.global_embed import error_embed
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
        except:
            await interaction.response.send_message(error_embed, ephemeral=True)
            return

        # Send welcome message
        with open(pixel_art_welcome_embed_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        embed_info = data['embeds'][0]
        embed_info['title'] = embed_info['title'].replace('[user]', interaction.user.name)
        embed_info['description'] = embed_info['description'].replace('[user]', interaction.user.name)
        embed_info['footer']['text'] = embed_info['footer']['text'].replace('[KEY]', ticket_id)
        embed = discord.Embed.from_dict(embed_info)

        await new_channel.send(f"{interaction.user.mention}",embed=embed)


        #Respond the message
        with open(ticket_success_embed_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for embed_info in data['embeds']:
            embed = discord.Embed.from_dict(embed_info)
        
        channel_id = new_channel.id
        await interaction.followup.send(embed=embed, view=jump_channel(guild_id, channel_id), ephemeral=True)
