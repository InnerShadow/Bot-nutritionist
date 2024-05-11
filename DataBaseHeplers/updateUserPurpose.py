import sqlite3 as sq

def update_user_purpose(chat_id: int, purpose: str) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET purpose=? WHERE chat_id=?", (purpose, chat_id))
        con.commit()


