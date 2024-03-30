from src.global_src.global_path import ticket_database_path
import sqlite3

def is_message_from_ticket(channel_id):
    conn = sqlite3.connect(ticket_database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pixel_art WHERE channel_id = ? AND close_time IS NULL', (channel_id,))
    ticket = cursor.fetchone()
    conn.close()
    return ticket is not None
