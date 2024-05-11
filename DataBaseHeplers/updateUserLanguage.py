import sqlite3 as sq

def update_user_language(chat_id: int, language: int) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET language=? WHERE chat_id=?", (language, chat_id))
        con.commit()

