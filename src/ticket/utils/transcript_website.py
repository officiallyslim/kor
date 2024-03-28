import discord
import chat_exporter

async def get_transcript(channel: discord.TextChannel):
    export = await chat_exporter.export(channel=channel)
    file_name=f"{channel.id}.html"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(export)
