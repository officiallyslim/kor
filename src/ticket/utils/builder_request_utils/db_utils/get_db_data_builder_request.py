import sqlite3
from src.global_src.global_path import ticket_database_path
from src.ticket.utils.builder_request_utils.db_utils.Ticket import Ticket

def get_builder_welcome_msg(ticket_id):
    conn = sqlite3.connect(ticket_database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT welcome_msg_id, channel_id FROM builder_request WHERE ticket_id = ? AND close_time IS NULL', (ticket_id,))
    welcome_msg_id, channel_id = cursor.fetchone()
    conn.close()
    return welcome_msg_id, channel_id

def get_builder_open_user_id(ticket_id):
    conn = sqlite3.connect(ticket_database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT open_user_id FROM builder_request WHERE ticket_id = ? AND close_time IS NULL', (str(ticket_id),))
    fetch_result = cursor.fetchone()
    conn.close()
    if fetch_result is not None:
        open_user_id = fetch_result[0]
        return open_user_id
    else:
        return None

def check_open_builder_ticket(user_id, ticket_type):
    conn = sqlite3.connect(ticket_database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT ticket_id, channel_id FROM builder_request WHERE open_user_id = ? AND close_time IS NULL AND ticket_type = ?', (user_id, ticket_type,))
    fetch_result = cursor.fetchone()
    conn.close()
    if fetch_result is not None:
        ticket_id, channel_id = fetch_result
        return ticket_id, channel_id
    else:
        return False

def check_claimed_builder_ticket(ticket_id):
    conn = sqlite3.connect(ticket_database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT claim_user_id FROM builder_request WHERE ticket_id = ? AND close_time IS NULL', (ticket_id,))
    fetch_result = cursor.fetchone()
    conn.close()
    if fetch_result is not None:
        claimed_users_id = fetch_result[0]
        return claimed_users_id
    else:
        return None

def get_builder_channel_id(ticket_id):
    conn = sqlite3.connect(ticket_database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT channel_id FROM builder_request WHERE ticket_id = ?', (str(ticket_id),))
    fetch_result = cursor.fetchone()
    conn.close()
    if fetch_result is not None:
        channel_id = fetch_result[0]
        return channel_id
    else:
        return None

def get_builder_queue_message_id(ticket_id):
    conn = sqlite3.connect(ticket_database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT queue_msg_id FROM builder_request WHERE ticket_id = ?', (ticket_id,))
    fetch_result = cursor.fetchone()
    conn.close()
    if fetch_result is not None:
        queue_msg_id = fetch_result[0]
        return queue_msg_id
    else:
        return None

def get_builder_log_message_id(ticket_id):
    conn = sqlite3.connect(ticket_database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT log_msg_id FROM builder_request WHERE ticket_id = ?', (ticket_id,))
    fetch_result = cursor.fetchone()
    conn.close()
    if fetch_result is not None:
        queue_msg_id = fetch_result[0]
        return queue_msg_id
    else:
        return None

def get_builder_dm_message_id(ticket_id):
    conn = sqlite3.connect(ticket_database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT open_user_id, dm_msg_id FROM builder_request WHERE ticket_id = ?', (ticket_id,))
    fetch_result = cursor.fetchone()
    conn.close()
    if fetch_result is not None:
        open_user_id = fetch_result[0]
        dm_msg_id = fetch_result[1]
        return open_user_id, dm_msg_id
    else:
        return None

def get_builder_confirm_message_id(ticket_id):
    conn = sqlite3.connect(ticket_database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT confirm_message_id FROM builder_request WHERE ticket_id = ?', (ticket_id,))
    fetch_result = cursor.fetchone()
    conn.close()
    if fetch_result is not None:
        confirm_message_id = fetch_result[0]
        return confirm_message_id
    else:
        return None

def get_builder_ticket_type(ticket_id):
    conn = sqlite3.connect(ticket_database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT ticket_type FROM builder_request WHERE ticket_id = ?', (ticket_id,))
    fetch_result = cursor.fetchone()
    conn.close()
    if fetch_result is not None:
        confirm_message_id = fetch_result[0]
        return confirm_message_id
    else:
        return None

def get_all_ticket_info(ticket_id):
    conn = sqlite3.connect(ticket_database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM builder_request WHERE ticket_id = ?', (ticket_id,))
    result = cursor.fetchone()
    conn.close()
    if result is not None:
        return Ticket(*result)
    else:
        return None