import discord
import json
from src.global_src.global_path import bss_codes_path

def loadCodes():
    try:
        with open(bss_codes_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

class showMoreModal(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.codes = loadCodes()
        self.add_item(self.create_select())

    def create_select(self):
        options = [
            discord.SelectOption(label=key) for key in self.codes.keys()
        ]
        select = discord.ui.Select(
            placeholder="Show me more about...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="dynamic_select",
        )
        select.callback = self.showMore_callback
        return select

    async def showMore_callback(self, interaction: discord.Interaction):
        codes = loadCodes()
        selected_key = interaction.data["values"][0]
        data = codes.get(selected_key)

        if data:
            reward = data.get("reward", "No reward specified.")
            day = data.get("added_date", "Unknown date.")
            location = data.get("location", "Unknown location.")

            responseEmbed = discord.Embed(
                title=f"{selected_key}",
                description=f"**Reward:** ```{reward}```\n"
                            f"**Released:** {day}\n"
                            f"**Location:** {location}",
                colour=discord.Colour(int("6798ed", 16)),
            )
            await interaction.response.send_message(embed=responseEmbed, ephemeral=True)
        else:
            await interaction.response.send_message("No data found for the selected code.", ephemeral=True)