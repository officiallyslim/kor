import discord

class form_pixel_art_modal(discord.ui.Modal):
    def __init__(self,name, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(
            label="Discord name",
            placeholder="Placeholder Test",
            min_length = 1,
            max_length = 30,
            style=discord.InputTextStyle.short,
            value=name))

        self.add_item(discord.ui.InputText(
            label="Roblox username",
            placeholder="Placeholder Test",
            min_length = 1,
            max_length = 30,
            style=discord.InputTextStyle.short))

        self.add_item(discord.ui.InputText(
            label="Island code",
            placeholder="Placeholder Test",
            min_length = 1,
            max_length = 10,
            style=discord.InputTextStyle.short))

        self.add_item(discord.ui.InputText(
            label="What build you need?",
            placeholder="Placeholder Test",
            min_length = 1,
            max_length = 400,
            row=3,
            style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Results")
        embed.add_field(name="Short Input", value=self.children[0].value)
        embed.add_field(name="Long Input", value=self.children[1].value)
        await interaction.response.send_message(embeds=[embed])