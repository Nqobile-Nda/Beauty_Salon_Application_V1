from models.db import database_connection, immediate_transaction


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


def booking_slot_has_conflict(date, time):
    conn, cur = database_connection()
    cur.execute(
        """
        SELECT request_id
        FROM booking_requests
        WHERE date = ?
          AND time = ?
          AND status IN ('Pending', 'Confirmed')
        LIMIT 1
        """,
        (date, time),
    )
    booking_conflict = cur.fetchone()

    cur.execute(
        """
        SELECT appointment_id
        FROM appointments
        WHERE date = ?
          AND time = ?
        LIMIT 1
        """,
        (date, time),
    )
    appointment_conflict = cur.fetchone()
    conn.close()
    return booking_conflict is not None or appointment_conflict is not None


def create_booking_request(status, selected_service, full_name, email, phone, date, time, message, created_at, created_by):
    booking_requests_table()
    with immediate_transaction() as (conn, cur):
        cur.execute(
            """
            SELECT request_id
            FROM booking_requests
            WHERE date = ?
              AND time = ?
              AND status IN ('Pending', 'Confirmed')
            LIMIT 1
            """,
            (date, time),
        )
        booking_conflict = cur.fetchone()

        cur.execute(
            """
            SELECT appointment_id
            FROM appointments
            WHERE date = ?
              AND time = ?
            LIMIT 1
            """,
            (date, time),
        )
        appointment_conflict = cur.fetchone()

        if booking_conflict or appointment_conflict:
            return False

        cur.execute("""
        INSERT INTO booking_requests (
            status, selected_service, full_name, email, phone, date, time, message, created_at, created_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (status, selected_service, full_name, email, phone, date, time, message, created_at, created_by))
        return True


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
