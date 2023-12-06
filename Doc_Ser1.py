import sqlite3

def connect_to_db():
    """
    Establishes a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A connection object to the database.
    """
    conn = sqlite3.connect('customer_database.db')
    return conn

def create_customer_table():
    """
    Creates the 'customers' table in the database if it does not exist.

    Prints a success message if the table is created, or an error message if the table creation fails.
    """
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY NOT NULL,
                full_name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                age INTEGER,
                address TEXT,
                gender TEXT,
                marital_status TEXT,
                wallet_balance REAL DEFAULT 0.0
            );
        ''')
        conn.commit()
        print("Customers table created successfully")
    except:
        print("Customers table creation failed - Maybe table already exists")
    finally:
        conn.close()

def insert_customer(customer):
    """
    Inserts a new customer into the 'customers' table.

    Args:
        customer (dict): A dictionary containing customer information.

    Returns:
        dict: A dictionary representing the inserted customer or an error message.
    """
    inserted_customer = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO customers (full_name, username, password, age, address, gender, marital_status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (customer['full_name'], customer['username'], customer['password'], customer['age'], customer['address'], customer['gender'], customer['marital_status']))
        conn.commit()
        inserted_customer = get_customer_by_username(customer['username'])
    except sqlite3.IntegrityError as e:
        conn.rollback()
        if "UNIQUE constraint failed: customers.username" in str(e):
            inserted_customer["error"] = "Username already taken. Please choose a different username."
        else:
            inserted_customer["error"] = "An error occurred while inserting the customer."
    finally:
        conn.close()

    return inserted_customer

def get_customers():
    """
    Retrieves a list of all customers from the 'customers' table.

    Returns:
        list: A list of dictionaries, each representing a customer.
    """
    customers_list = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM customers")
        rows = cur.fetchall()
        for row in rows:
            customer = dict(row)
            customers_list.append(customer)
    except:
        customers_list = []

    return customers_list

def get_customer_by_username(username):
    """
    Retrieves a customer by their username from the 'customers' table.

    Args:
        username (str): The username of the customer.

    Returns:
        dict: A dictionary representing the customer or an empty dictionary if not found.
    """
    customer = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM customers WHERE username = ?", (username,))
        row = cur.fetchone()
        if row:
            customer = dict(row)
    except:
        customer = {}

    return customer

def update_customer(customer):
    """
    Updates customer information in the 'customers' table.

    Args:
        customer (dict): A dictionary containing updated customer information.

    Returns:
        dict: A dictionary representing the updated customer or an empty dictionary if an error occurs.
    """
    updated_customer = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        update_query = "UPDATE customers SET "
        update_values = []
        for key, value in customer.items():
            if key not in ['id', 'username', 'password', 'wallet_balance']:
                update_query += f"{key} = ?, "
                update_values.append(value)
        update_query = update_query.rstrip(', ') + " WHERE id = ?"
        update_values.append(customer["id"])
        cur.execute(update_query, tuple(update_values))
        conn.commit()
        updated_customer = get_customer_by_username(customer['username'])
    except:
        conn.rollback()
    finally:
        conn.close()

    return updated_customer

def delete_customer(customer_id):
    """
    Deletes a customer from the 'customers' table.

    Args:
        customer_id (int): The ID of the customer to be deleted.

    Returns:
        dict: A dictionary containing a status message.
    """
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        conn.commit()
        message["status"] = "Customer deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete customer"
    finally:
        conn.close()

    return message

def charge_wallet(username, amount):
    """
    Charges a customer's wallet in the 'customers' table.

    Args:
        username (str): The username of the customer.
        amount (float): The amount to be added to the wallet.

    Returns:
        dict: A dictionary containing a status message.
    """
    message = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE customers SET wallet_balance = wallet_balance + ? WHERE username = ?", (amount, username))
        conn.commit()
        message["status"] = "Wallet charged successfully"
    except:
        conn.rollback()
        message["status"] = "Error charging wallet"
    finally:
        conn.close()

    return message

def deduct_wallet(username, amount):
    """
    Deducts money from a customer's wallet in the 'customers' table.

    Args:
        username (str): The username of the customer.
        amount (float): The amount to be deducted from the wallet.

    Returns:
        dict: A dictionary containing a status message.
    """
    message = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT wallet_balance FROM customers WHERE username = ?", (username,))
        current_balance = cur.fetchone()[0]
        if current_balance >= amount:
            new_balance = current_balance - amount
            cur.execute("UPDATE customers SET wallet_balance = ? WHERE username = ?", (new_balance, username))
            conn.commit()
            message["status"] = "Money deducted successfully"
        else:
            message["status"] = "Insufficient funds in the wallet"
    except:
        conn.rollback()
        message["status"] = "Error deducting money"
    finally:
        conn.close()

    return message

# Initialize customers table
create_customer_table()