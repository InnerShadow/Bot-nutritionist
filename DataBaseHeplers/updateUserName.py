import sqlite3 as sq

def update_user_name(chat_id: int, name: str) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET name=? WHERE chat_id=?", (name, chat_id))
        con.commit()

