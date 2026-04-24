import sqlite3


def database_connection():
    conn = sqlite3.connect("CBL.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()
    return conn, cur


def booking_requests_table():
    conn, cur = database_connection()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS booking_requests (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        status TEXT NOT NULL,
        selected_service TEXT NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT NOT NULL,
        created_by TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()


def create_booking_request(status, selected_service, full_name, email, phone, date, time, message, created_at, created_by):
    booking_requests_table()
    conn, cur = database_connection()
    cur.execute("""
    INSERT INTO booking_requests (
        status, selected_service, full_name, email, phone, date, time, message, created_at, created_by
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (status, selected_service, full_name, email, phone, date, time, message, created_at, created_by))
    conn.commit()
    conn.close()


def load_user_booking_requests():
    booking_requests_table()
    conn, cur = database_connection()
    cur.execute("SELECT * FROM booking_requests ORDER BY request_id DESC")
    booking_requests = [dict(row) for row in cur.fetchall()]
    conn.close()
    return booking_requests


def load_specific_user_booking_request(request_id):
    booking_requests_table()
    conn, cur = database_connection()
    cur.execute("SELECT * FROM booking_requests WHERE request_id = ?", (request_id,))
    booking_request = cur.fetchone()
    conn.close()
    return dict(booking_request) if booking_request else None


def update_user_booking_request_status(request_id, status):
    booking_requests_table()
    conn, cur = database_connection()
    cur.execute(
        "UPDATE booking_requests SET status = ? WHERE request_id = ?",
        (status, request_id),
    )
    updated = cur.rowcount > 0
    conn.commit()
    conn.close()
    return updated
