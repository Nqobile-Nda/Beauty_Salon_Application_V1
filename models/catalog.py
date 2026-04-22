import sqlite3

def database_connection():
    conn = sqlite3.connect("CBL.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur


def catalog_table():
    conn, cur = database_connection()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS catalog (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price TEXT NOT NULL,
    category TEXT NOT NULL,
    image BLOB NOT NULL,
    description TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL    
    );
    """)
    conn.commit()
    conn.close()


def load_catalog():
    catalog_table()
    conn, cur = database_connection()
    cur.execute("""
    SELECT * FROM catalog ORDER BY item_id DESC
    """)
    catalog = [dict(row) for row in cur.fetchall()]
    conn.close()
    return catalog


def add_item(name, price, category, image, description, created_at, created_by):
    catalog_table()
    conn, cur = database_connection()
    cur.execute("""
    INSERT INTO catalog (name, price, category, image, description, created_at, created_by) VALUES (?,?,?,?,?,?,?)
    """, (name, price, category, image, description, created_at, created_by))
    conn.commit()
    conn.close()


def update_item_details(item_id, name, price, category, image, description, created_at, created_by):
    catalog_table()
    catalog = load_catalog()
    item = [item for item in catalog if item.get("item_id") == item_id]
    item["name"] = name
    item["price"] = price
    item["category"] = category