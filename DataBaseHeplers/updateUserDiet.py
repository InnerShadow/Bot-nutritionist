import sqlite3 as sq

def update_user_diet(chat_id: int, diet: str) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET diet=? WHERE chat_id=?", (diet, chat_id))
        con.commit()

