import os
import sqlite3
from contextlib import contextmanager


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "CBL.db")


def database_connection():
    conn = sqlite3.connect(DATABASE_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    conn.execute("PRAGMA busy_timeout = 5000")
    return conn, conn.cursor()


@contextmanager
def immediate_transaction():
    conn, cur = database_connection()
    try:
        conn.execute("BEGIN IMMEDIATE")
        yield conn, cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def initialize_database_performance():
    conn, cur = database_connection()
    cur.executescript(
        """
        CREATE INDEX IF NOT EXISTS idx_booking_requests_date_time
            ON booking_requests(date, time);

        CREATE INDEX IF NOT EXISTS idx_booking_requests_status
            ON booking_requests(status);

        CREATE INDEX IF NOT EXISTS idx_booking_requests_created_at
            ON booking_requests(created_at);

        CREATE INDEX IF NOT EXISTS idx_appointments_date_time
            ON appointments(date, time);

        CREATE INDEX IF NOT EXISTS idx_appointments_request_id
            ON appointments(request_id);

        CREATE INDEX IF NOT EXISTS idx_catalog_category
            ON catalog(category);
        """
    )
    conn.commit()
    conn.close()
