import sqlite3

def connect_to_db():
    conn = sqlite3.connect('inventory.db')
    return conn

def create_goods_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE goods (
                id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                description TEXT,
                count INTEGER NOT NULL
            );
        ''')
        conn.commit()
        print("Goods table created successfully")
    except:
        print("Goods table creation failed - Maybe table already exists")
    finally:
        conn.close()

def insert_goods(goods):
    inserted_goods = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO goods (name, category, price, description, count) VALUES (?, ?, ?, ?, ?)",
                    (goods['name'], goods['category'], goods['price'], goods['description'], goods['count']))
        conn.commit()
        inserted_goods = get_goods_by_id(cur.lastrowid)
    except:
        conn.rollback()
    finally:
        conn.close()

    return inserted_goods

def get_goods():
    goods_list = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM goods")
        rows = cur.fetchall()
        for row in rows:
            goods = dict(row)
            goods_list.append(goods)
    except:
        goods_list = []

    return goods_list

def get_goods_by_id(goods_id):
    goods = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM goods WHERE id = ?", (goods_id,))
        row = cur.fetchone()
        if row:
            goods = dict(row)
    except:
        goods = {}

    return goods

def update_goods(goods):
    updated_goods = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE goods SET name = ?, category = ?, price = ?, description = ?, count = ? WHERE id = ?",
                    (goods["name"], goods["category"], goods["price"], goods["description"], goods["count"], goods["id"]))
        conn.commit()
        updated_goods = get_goods_by_id(goods["id"])
    except:
        conn.rollback()
    finally:
        conn.close()

    return updated_goods

def deduct_goods(goods_id):
    message = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE from goods WHERE id = ?", (goods_id,))
        conn.commit()
        message["status"] = "Goods deducted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot deduct goods"
    finally:
        conn.close()

    return message

# Initialize goods table
create_goods_table()

# Example goods data
goods_data = {
    "name": "Laptop",
    "category": "electronics",
    "price": 1200.00,
    "description": "High-performance laptop",
    "count": 10
}
