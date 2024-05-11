import sqlite3 as sq

def check_chat_existance(chat_id : int) -> bool:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE chat_id=?", (chat_id,))
        count = cur.fetchone()
        return True if count is not None else False
    
