import sqlite3

def database_connection():
    conn = sqlite3.connect("CBL.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur


def admins_table():
    conn, cur = database_connection()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins_table (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL,
    password TEXT NOT NULL,
    login_history TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()
