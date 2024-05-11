import sqlite3 as sq

def get_users_data(chat_id : int) -> str:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE chat_id=?", (chat_id,))
        user_data = cur.fetchone()
        
        return user_data
    
