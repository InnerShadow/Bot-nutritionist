import sqlite3 as sq

def initDataBase():
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        chat_id INTEGER,
                        gender INTEGER,
                        height FLOAT,
                        weight FLOAT,
                        name TEXT,
                        purpose TEXT,
                        language TEXT,
                        age FLOAT,
                        UNIQUE(chat_id)
                        )""")
        
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS MessageHistory (
                        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        message TEXT,
                        role TEXT,
                        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                        )""")

            
def insertMessage(chat_id : int, message : str, role : str) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users WHERE chat_id = ?", (chat_id,))
        user_id = cur.fetchone()
        
        user_id = user_id[0]
        cur.execute("SELECT COUNT(*) FROM MessageHistory WHERE user_id = ?", (user_id,))
        message_count = cur.fetchone()[0]
        
        if message_count >= 10:
            cur.execute("DELETE FROM MessageHistory WHERE user_id = ? ORDER BY sent_at ASC LIMIT 1", (user_id,))
        
        cur.execute("INSERT INTO MessageHistory (user_id, message, role) VALUES (?, ?, ?)", (user_id, message, role))
        con.commit()

def getMessageHistory(chat_id : int) -> list:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users WHERE chat_id = ?", (chat_id,))
        user_id = cur.fetchone()
        if user_id:
            user_id = user_id[0]
            cur.execute("SELECT message, role FROM MessageHistory WHERE user_id = ? ORDER BY sent_at DESC", (user_id, ))
            message_history = cur.fetchall()
            return message_history
        else:
            return []

def create_user(chat_id) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM users WHERE chat_id=?", (chat_id,))
        count = cur.fetchone()[0]
        if count == 0:
            cur.execute("INSERT INTO users (chat_id) VALUES (?)", (chat_id,))
            con.commit()


def update_user_language(chat_id: int, language: int) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET language=? WHERE chat_id=?", (language, chat_id))
        con.commit()


def update_user_gender(chat_id: int, gender: int) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET gender=? WHERE chat_id=?", (gender, chat_id))
        con.commit()


def update_user_age(chat_id: int, age: float) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET age=? WHERE chat_id=?", (age, chat_id))
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


def update_user_purpose(chat_id: int, purpose: str) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET purpose=? WHERE chat_id=?", (purpose, chat_id))
        con.commit()


def update_user_name(chat_id: int, name: str) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET name=? WHERE chat_id=?", (name, chat_id))
        con.commit()

def get_users_data(chat_id : int) -> str:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE chat_id=?", (chat_id,))
        user_data = cur.fetchone()
        
        return user_data

def check_chat_existance(chat_id : int) -> bool:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE chat_id=?", (chat_id,))
        count = cur.fetchone()
        return True if count is not None else False