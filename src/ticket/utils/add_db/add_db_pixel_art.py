import sqlite3
from src.global_src.global_path import ticket_database_path

def add_db_pixel_art(ticket_id, open_user_id, open_time, open_reason, form_name, form_roblox_user, form_island_code, form_build, form_build_desp, form_build_img, channel_id, welcome_msg_id, dm_msg_id, queue_msg_id, log_msg_id, claim_status, claim_user_id, close_user_id, close_time, close_reason):
    conn = sqlite3.connect(ticket_database_path)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO pixel_art (ticket_id, open_user_id, open_time, open_reason, form_name, form_roblox_user, form_island_code, form_build, form_build_desp, form_build_img, channel_id, welcome_msg_id, dm_msg_id, queue_msg_id, log_msg_id, claim_status, claim_user_id, close_user_id, close_time, close_reason)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (ticket_id, open_user_id, open_time, open_reason, form_name, form_roblox_user, form_island_code, form_build, form_build_desp, form_build_img, channel_id, welcome_msg_id, dm_msg_id, queue_msg_id, log_msg_id, claim_status, claim_user_id, close_user_id, close_time, close_reason))
    
    conn.commit()
    conn.close()