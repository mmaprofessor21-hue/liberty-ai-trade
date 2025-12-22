# P25-06-04_14-47-51
import sqlite3

def init_db():
    conn = sqlite3.connect("liberty_trade.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT,
        amount REAL,
        action TEXT,
        timestamp TEXT
    )
    """)
    conn.commit()
    conn.close()
