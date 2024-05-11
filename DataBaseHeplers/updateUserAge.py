import sqlite3 as sq

def update_user_age(chat_id: int, age: float) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET age=? WHERE chat_id=?", (age, chat_id))
        con.commit()

