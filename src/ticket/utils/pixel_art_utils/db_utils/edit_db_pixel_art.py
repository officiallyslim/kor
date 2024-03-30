import sqlite3
from src.global_src.global_path import ticket_database_path

def edit_db_pixel_art(ticket_id, **kwargs):
    conn = sqlite3.connect(ticket_database_path)
    cursor = conn.cursor()
    
    # Start edit
    query = "UPDATE pixel_art SET "
    update_values = []
    
    # Add args
    for key, value in kwargs.items():
        query += f"{key} = ?, "
        update_values.append(value)
    
    # Add to variables
    query = query.rstrip(', ')
    query += " WHERE ticket_id = ?"
    update_values.append(ticket_id)
    
    # Send
    cursor.execute(query, update_values)
    
    conn.commit()
    conn.close()