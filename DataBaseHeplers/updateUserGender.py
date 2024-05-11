import sqlite3 as sq

def update_user_gender(chat_id: int, gender: int) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET gender=? WHERE chat_id=?", (gender, chat_id))
        con.commit()

