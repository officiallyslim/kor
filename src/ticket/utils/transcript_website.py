import discord
import chat_exporter

async def get_transcript(channel: discord.TextChannel, ticket_id):
    print(f"Creating transcript for {ticket_id}...")
    await chat_exporter.export(channel=channel)
    file_name=f"db/ticket/transcript/{ticket_id}.html"

    print(f"Exported to {file_name}")