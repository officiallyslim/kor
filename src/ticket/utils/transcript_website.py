import discord
import chat_exporter
import dotenv
import os
import requests
from src.ticket.utils.gen_ticket_key import gen_key

# Github token
dotenv.load_dotenv()
private_api = str(os.getenv("PRIVATE_API"))
private_api_token = str(os.getenv("PRIVATE_API_KEY_TOKEN"))

async def get_transcript(channel: discord.TextChannel, ticket_id):
    export = await chat_exporter.export(channel=channel)
    file_name=f"db/ticket/transcript/{ticket_id}.html"

    if not os.path.exists(file_name):
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(export)
    else:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(export)

    # Upload transcript to private server
    # print(f"Uploading transcript {ticket_id} to private API server.")
    private_api_url= f"{private_api}/addTranscript"

    with open(file_name, 'r', encoding='utf-8') as f:
        html_data = f.read()

    headers = {
        'Authorization': private_api_token
    }

    # Gen ticket_key
    ticket_key = gen_key(10)

    data = {
        'html': html_data,
        'ticket_id': ticket_id,
        'ticket_key': ticket_key
    }

    response = requests.post(private_api_url, headers=headers, json=data)

    if response.status_code == 201:
        print(f"Transcript {ticket_id} sent correctly!")
        return [
            f"{private_api}/getTranscript/{ticket_id}?ticket_key={ticket_key}",
            ticket_key,
        ]
    else:
        print('Error sending transcript:', response.status_code, response.text)
        return [
            "Failed",
            ticket_key,
        ]
