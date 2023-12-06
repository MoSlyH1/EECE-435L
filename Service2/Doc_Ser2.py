import sqlite3

def connect_to_db():
    """
    Establishes a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A connection object to the database.
    """
    conn = sqlite3.connect('inventory.db')
    return conn

def create_goods_table():
    """
    Creates the 'goods' table in the database if it does not exist.

    Prints a success message if the table is created, or an error message if the table creation fails.
    """
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS goods (
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
    """
    Inserts new goods into the 'goods' table.

    Args:
        goods (dict): A dictionary containing goods information.

    Returns:
        dict: A dictionary representing the inserted goods or an empty dictionary if an error occurs.
    """
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
    """
    Retrieves a list of all goods from the 'goods' table.

    Returns:
        list: A list of dictionaries, each representing goods information.
    """
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
    """
    Retrieves goods by their ID from the 'goods' table.

    Args:
        goods_id (int): The ID of the goods.

    Returns:
        dict: A dictionary representing the goods or an empty dictionary if not found.
    """
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
    """
    Updates goods information in the 'goods' table.

    Args:
        goods (dict): A dictionary containing updated goods information.

    Returns:
        dict: A dictionary representing the updated goods or an empty dictionary if an error occurs.
    """
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
    """
    Deducts goods from the 'goods' table.

    Args:
        goods_id (int): The ID of the goods to be deducted.

    Returns:
        dict: A dictionary containing a status message.
    """
    message = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM goods WHERE id = ?", (goods_id,))
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
