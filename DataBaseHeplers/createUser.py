import sqlite3 as sq

def create_user(chat_id : int) -> None:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM users WHERE chat_id=?", (chat_id,))
        count = cur.fetchone()[0]
        if count == 0:
            cur.execute(f"INSERT INTO users (chat_id, gender, height, purpose, language, age, diet) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                        (chat_id, get_mode("gender"), get_median("height"), "Improve my health", "English", get_median("age"), "No diet"))
            con.commit()


def get_mode(column : str) -> str:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute(f"SELECT {column}, COUNT(*) AS frequency FROM users GROUP BY {column} ORDER BY frequency DESC LIMIT 1;")
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            return None


def get_median(column : str) -> float:
    with sq.connect("Data/database.db") as con:
        cur = con.cursor()
        cur.execute(f"""SELECT AVG({column}) AS median
                        FROM (
                            SELECT {column},
                                ROW_NUMBER() OVER (ORDER BY {column}) AS row_num,
                                COUNT(*) OVER () AS total_rows
                            FROM users
                        ) AS subquery
                        WHERE row_num IN (FLOOR((total_rows + 1) / 2), CEIL((total_rows + 1) / 2));
                        """)
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            return None