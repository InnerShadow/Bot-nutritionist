import sqlite3 as sq

def update_user_height(chat_id: int, height: float) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET height=? WHERE chat_id=?", (height, chat_id))
        con.commit()

