import sqlite3 as sq

def get_language(chat_id : int) -> int:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT language FROM users WHERE chat_id=?", (chat_id,))
        language = cur.fetchone()[0]
        if language == "English":
            return 0
        elif language == "Русский":
            return 1
        else:
            return 2
        
