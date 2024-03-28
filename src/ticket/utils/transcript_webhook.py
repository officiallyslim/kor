import discord
from config import bot
import sqlite3
from src.global_src.global_path import ticket_database_path
import requests
import json
from src.ticket.utils.db_utils.edit_db_pixel_art import edit_db_pixel_art

def embed_to_dict(embed):
    embed_dict = {
        "title": embed.title,
        "description": embed.description,
        "color": embed.color.value if embed.color else None,  # Convierte el color a un valor entero
        "fields": [{"name": field.name, "value": field.value, "inline": field.inline} for field in embed.fields],
    }

    if embed.footer:
        embed_dict["footer"] = {"text": embed.footer.text}
    if embed.image:
        embed_dict["image"] = {"url": embed.image.url}
    if embed.thumbnail:
        embed_dict["thumbnail"] = {"url": embed.thumbnail.url}

    return embed_dict


def send_discord_message(profile, thread_id, name, message_content, embeds):
    webhook_url = f"https://discord.com/api/webhooks/1222702893463765173/tx2nGBzu1CsO002I5l7rY5HjHD9HW6cydEE3ZpT_UCzNqjN9TlJeBp7JItR2lP8pv3BB?thread_id={thread_id}"
    # Message format
    data = {
        "avatar_url": profile,
        "username": name,
        "content": message_content,
        "embeds": [embed_to_dict(embed) for embed in embeds]
    }

    # Send msg
    response = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})

    # Retry
    if response.status_code != 204:
        raise ValueError(f"Request to Discord returned an error {response.status_code}, the response is:\n{response.text}")


async def transcript(message: discord.Message):
    # Connect to the database
    conn = sqlite3.connect(ticket_database_path)
    cursor = conn.cursor()

    # Check if the ticket has a transcript_thread_id and get others information
    cursor.execute('SELECT transcript_thread_id, ticket_id, open_user_id FROM pixel_art WHERE channel_id = ?', (message.channel.id,))
    ticket = cursor.fetchone()

    # Close the database connection
    conn.close()

    # Si 'ticket' no es None, entonces hay datos para almacenar
    if ticket is not None:
        transcript_thread_id = ticket[0]
        ticket_id = ticket[1]
        open_user_id = ticket[2]
        # Ahora puedes usar las variables 'transcript_thread_id', 'ticket_id' y 'open_user_id' en tu código
    else:
        # No se encontraron datos
        print("No se encontraron registros para el channel_id proporcionado.")


    user = bot.get_user(message.author.id)
    if user.avatar:
        pfp_url = str(user.avatar.url)
    else:
        pfp_url = "https://discord.com/assets/1f0bfc0865d324c2587920a7d80c609b.png"

    print(pfp_url)
    log_channel = bot.get_channel(1222548503251648522)

    # Check if the ticket has a transcript_thread_id
    if transcript_thread_id is not None:
        print(f"El ticket en el canal {message.channel.id} tiene un transcript_thread_id: {ticket[0]}")
        send_discord_message(pfp_url, transcript_thread_id, user.name, message.content, message.embeds)
    else:
        print(f"El ticket en el canal {message.channel.id} no tiene un transcript_thread_id asociado.")
        thread = await log_channel.create_thread(name=f"Pixel Art Request - {ticket_id} - {open_user_id}", content="Starting new transcript...")
        send_discord_message(pfp_url,thread.id, user.name, message.content, message.embeds)
        print(thread.id)
        edit_db_pixel_art(
        ticket_id=ticket_id,
        transcript_thread_id=thread.id,
        )
