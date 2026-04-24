import sqlite3


def database_connection():
    conn = sqlite3.connect("CBL.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()
    return conn, cur


def appointments_table():
    conn, cur = database_connection()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER,
    selected_service TEXT NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL, 
    phone TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL, 
    message TEXT NOT NULL,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
                
    FOREIGN KEY (request_id) REFERENCES booking_requests(request_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    );
    """)

    conn.commit()
    conn.close()


def load_appointments():
    appointments_table()
    conn, cur = database_connection()
    cur.execute("""
    SELECT * FROM appointments
    """)
    appointments = [dict(row) for row in cur.fetchall()]

    conn.commit()
    conn.close()
    return appointments


def create_appointment(request_id, selected_service, full_name, email, phone, date, time, message, created_at, created_by):
    appointments_table()
    conn, cur = database_connection()

    cur.execute("""
    INSERT INTO appointments (
    request_id, selected_service, full_name, email, phone, date, time, message, created_at, created_by
    ) VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (request_id, selected_service, full_name, email, phone, date, time, message, created_at, created_by))

    if request_id is not None:
        cur.execute("""
        UPDATE booking_requests SET status = ? WHERE request_id = ?
        """, ("Confirmed", request_id))

    conn.commit()
    conn.close()


def load_specific_appointment(appointment_id):
    appointments_table()
    conn, cur = database_connection()

    cur.execute("""
    SELECT * FROM appointments WHERE appointment_id = ?
    """, (appointment_id,))
    row = cur.fetchone()
    specified_appointment = dict(row) if row else None

    conn.close()
    return specified_appointment


def completed_appointment(appointment_id, request_id):
    appointments_table()
    conn, cur = database_connection()
    cur.execute("""
    DELETE FROM appointments WHERE appointment_id = ?
    """, (appointment_id,))

    cur.execute("""
    UPDATE booking_requests SET status = ? WHERE request_id = ?
    """, ("Completed", request_id))

    conn.commit()
    conn.close()


def cancelled_appointment(appointment_id, request_id):
    appointments_table()
    conn, cur = database_connection()
    cur.execute("""
    DELETE FROM appointments WHERE appointment_id = ?
    """, (appointment_id,))

    cur.execute("""
    UPDATE booking_requests SET status = ? WHERE request_id = ?
    """, ("Cancelled", request_id))

    conn.commit()
    conn.close()
