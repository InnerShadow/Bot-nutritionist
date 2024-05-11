import sqlite3 as sq

def update_user_weight(chat_id: int, weight: float) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET weight=? WHERE chat_id=?", (weight, chat_id))
        con.commit()

