import sqlite3 as sq

def initDataBase():
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        chat_id INTEGER,
                        gender TEXT,
                        height FLOAT,
                        weight FLOAT,
                        name TEXT,
                        purpose TEXT,
                        language TEXT,
                        age FLOAT,
                        diet TEXT, 
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
        
