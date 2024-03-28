import discord
from src.global_src.global_emojis import send_emoji

from src.global_src.embed_to_dict import embed_to_dict

class confirm_form_pixel_art_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) 

    @discord.ui.button(label="Send", style=discord.ButtonStyle.green, emoji=send_emoji, custom_id="send_form_pixel_art_view")
    async def send_form_pixel_art_view(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    @discord.ui.button(label="Edit", style=discord.ButtonStyle.gray, emoji="✏️", custom_id="edit_form_pixel_art_view")
    async def edit_form_pixel_art_view(self, button: discord.ui.Button, interaction: discord.Interaction):
        from src.ticket.modal.form_pixel_art import form_pixel_art_modal

        # Get old data
        embed = [embed_to_dict(embed) for embed in interaction.message.embeds]
        name = embed[0]['fields'][0]['value'].replace("```", "")
        roblox_username = embed[0]['fields'][1]['value'].replace("```", "")
        island_code = embed[0]['fields'][2]['value'].replace("```", "")
        build = embed[0]['fields'][3]['value'].replace("```", "")
        modal = form_pixel_art_modal(title="Pixel Art Form", name=name, status="edit", roblox_user=roblox_username, island_code=island_code, build=build)
        await interaction.response.send_modal(modal)