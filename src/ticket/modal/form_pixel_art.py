import discord
from src.ticket.view.confirm_form_pixel_art import confirm_form_pixel_art_view

class form_pixel_art_modal(discord.ui.Modal):
    def __init__(self, name, roblox_user=None, island_code=None, build=None, status=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.status = status

        self.add_item(discord.ui.InputText(
            label="Discord name",
            placeholder="Your discord name",
            min_length = 1,
            max_length = 30,
            style=discord.InputTextStyle.short,
            value=name
            ))

        self.add_item(discord.ui.InputText(
            label="Roblox username",
            placeholder="Your roblox username",
            min_length = 1,
            max_length = 30,
            style=discord.InputTextStyle.short,
            value=roblox_user
            ))

        self.add_item(discord.ui.InputText(
            label="Island code",
            placeholder="Your Roblox Island Code",
            min_length = 1,
            max_length = 10,
            style=discord.InputTextStyle.short,
            value=island_code
            ))

        self.add_item(discord.ui.InputText(
            label="What build you need?",
            placeholder="What build is in your mind?",
            min_length = 1,
            max_length = 400,
            row=3,
            style=discord.InputTextStyle.long,
            value=build
            ))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Pixel Art form answers")
        embed.add_field(name="Discord name", value=f"```{self.children[0].value}```", inline=False)
        embed.add_field(name="Roblox username", value=f"```{self.children[1].value}```", inline=False)
        embed.add_field(name="Island Code", value=f"```{self.children[2].value}```", inline=False)
        embed.add_field(name="Build", value=f"```{self.children[3].value}```", inline=False)

        if self.status == "new":
            await interaction.response.send_message(content="Please, confirm your answer before send to moderators", embeds=[embed], view=confirm_form_pixel_art_view())
        elif self.status == "edit":
            await interaction.response.edit_message(content="Please, confirm your answer before send to moderators", embeds=[embed], view=confirm_form_pixel_art_view())
