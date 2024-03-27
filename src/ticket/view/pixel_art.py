import discord
from src.global_src.global_emojis import smile_pixel_emoji
from src.ticket.utils.create_overwrites import create_overwrites
from typing import Union

class pixel_art_panel_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Pixel Art", style=discord.ButtonStyle.primary, emoji=smile_pixel_emoji, custom_id="pixel_art_panel_button")
    async def pixel_art_panel_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        print("Creating new ticket")
        member_who_interacted = interaction.user
        mod_role = interaction.guild.get_role(1222579667207192626)

        # Crea una tupla con los objetos que quieres incluir en los overwrites.
        objects = (member_who_interacted, mod_role)

        # Llama a la función create_overwrites con los objetos desempaquetados.
        overwrites = create_overwrites(interaction, *objects)

        # Ahora puedes crear el canal de texto con los overwrites.
        await interaction.guild.create_text_channel(
            name="nombre_del_canal",
            overwrites=overwrites,
            topic="Descripción del canal",
            reason="Razón para crear el canal",
            category=discord.Object(id=1222316215884582924)  # Asegúrate de que este ID de categoría sea correcto
        )
