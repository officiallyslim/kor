import sqlite3
from src.global_src.global_path import ticket_database_path

def get_welcome_msg(ticket_id):
    conn = sqlite3.connect(ticket_database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT welcome_msg_id, channel_id FROM pixel_art WHERE ticket_id = ? AND close_time IS NULL', (ticket_id,))
    welcome_msg_id, channel_id = cursor.fetchone()
    conn.close()
    return welcome_msg_id, channel_id

def get_open_user_id(ticket_id):
    conn = sqlite3.connect(ticket_database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT open_user_id FROM pixel_art WHERE ticket_id = ? AND close_time IS NULL', (ticket_id,))
    open_user_id = cursor.fetchone()
    conn.close()
    return open_user_id
