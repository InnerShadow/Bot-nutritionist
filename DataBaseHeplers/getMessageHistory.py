import sqlite3 as sq

def getMessageHistory(chat_id : int) -> list:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users WHERE chat_id = ?", (chat_id,))
        user_id = cur.fetchone()
        if user_id:
            user_id = user_id[0]
            cur.execute("SELECT message, role FROM MessageHistory WHERE user_id = ? ORDER BY sent_at DESC", (user_id, ))
            message_history = cur.fetchall()
            return message_history
        else:
            return []
        
