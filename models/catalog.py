from models.db import database_connection


def catalog_table():
    conn, cur = database_connection()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS catalog (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price TEXT NOT NULL,
    category TEXT NOT NULL,
    image TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL    
    );
    """)

    cur.execute("""SELECT * FROM catalog""")
    item = cur.fetchone()
    if not item:
        cur.execute("""
        INSERT INTO catalog (name, price, category, image, description, created_at, updated_at) VALUES (?,?,?,?,?,?,?)
        """, ("Nqobile", "200", "Wigs", "images/ImageError.webp", "Hi", "2006-12-12 08:12:12", "2006-12-12 08:12:12"))

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


def load_filtered_catalog(category):
    catalog_table()
    conn, cur = database_connection()
    cur.execute("""
    SELECT * FROM catalog WHERE category = ?  
    """, (category,))
    filtered_catalog = [dict(row) for row in cur.fetchall()]
    conn.commit()
    conn.close()
    return filtered_catalog


def add_item(name, price, category, image, description, created_at, updated_at):
    catalog_table()
    conn, cur = database_connection()
    cur.execute("""
    INSERT INTO catalog (name, price, category, image, description, created_at, updated_at) VALUES (?,?,?,?,?,?,?)
    """, (name, price, category, image, description, created_at, updated_at))
    conn.commit()
    conn.close()


def update_item_details(item_id, name, price, category, image, description, created_at, updated_at):
    catalog_table()
    conn, cur = database_connection()
    cur.execute("""
    UPDATE catalog SET name=?, price=?, category=?, image=?, description=?, created_at=?, updated_at=? WHERE item_id=?
    """, (name, price, category, image, description, created_at, updated_at, item_id))
    conn.commit()
    conn.close()


def delete_item(item_id):
    catalog_table()
    conn, cur = database_connection()
    cur.execute("""
    DELETE FROM catalog WHERE item_id=?
    """, (item_id,))
    conn.commit()
    conn.close()
