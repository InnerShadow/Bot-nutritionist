import sqlite3 as sq

def insertMessage(chat_id : int, message : str, role : str) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users WHERE chat_id = ?", (chat_id,))
        user_id = cur.fetchone()
        
        user_id = user_id[0]
        cur.execute("SELECT COUNT(*) FROM MessageHistory WHERE user_id = ?", (user_id,))
        message_count = cur.fetchone()[0]
        
        if message_count >= 10:
            cur.execute("DELETE FROM MessageHistory WHERE user_id = ? ORDER BY sent_at ASC LIMIT 1", (user_id,))
        
        cur.execute("INSERT INTO MessageHistory (user_id, message, role) VALUES (?, ?, ?)", (user_id, message, role))
        con.commit()

