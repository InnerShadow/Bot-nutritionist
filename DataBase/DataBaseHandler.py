import sqlite3 as sq

def initDataBase():
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        chat_id INTEGER,
                        sex INTEGER,
                        height FLOAT,
                        weight FLOAT,
                        name TEXT,
                        purpose TEXT,
                        language INT,
                        UNIQUE(chat_id)
                        )""")
        
def create_user(chat_id: int, language: str) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO users (chat_id, language) VALUES (?, ?)", (chat_id, language))
        con.commit()


def update_user_sex(chat_id: int, sex: int) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET sex=? WHERE chat_id=?", (sex, chat_id))
        con.commit()


def update_user_height(chat_id: int, height: float) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET height=? WHERE chat_id=?", (height, chat_id))
        con.commit()


def update_user_weight(chat_id: int, weight: float) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET weight=? WHERE chat_id=?", (weight, chat_id))
        con.commit()

