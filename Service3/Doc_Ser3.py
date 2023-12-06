import requests
import sqlite3

# URLs for the customer and goods services
CUSTOMER_SERVICE_URL = "http://localhost:5001"  # Update with the actual URL of the customer service
GOODS_SERVICE_URL = "http://localhost:5002"     # Update with the actual URL of the goods service

# Database setup
def connect_to_db():
    """
    Establishes a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A connection object to the database.
    """
    conn = sqlite3.connect('purchase_history.db')
    return conn

def create_purchase_history_table():
    """
    Creates the 'purchase_history' table in the database if it does not exist.

    Prints a success message if the table is created, or an error message if the table creation fails.
    """
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS purchase_history (
                id INTEGER PRIMARY KEY NOT NULL,
                customer_username TEXT NOT NULL,
                good_name TEXT NOT NULL,
                good_price REAL NOT NULL,
                timestamp TIMESTAMP NOT NULL
            );
        ''')
        conn.commit()
        print("Purchase history table created successfully")
    except:
        print("Purchase history table creation failed - Maybe table already exists")
    finally:
        conn.close()

# Initialize purchase history table
create_purchase_history_table()

def display_available_goods():
    """
    Retrieves a list of available goods from the goods service.

    Returns:
        list: A list of dictionaries containing information about available goods.
    """
    try:
        response = requests.get(f"{GOODS_SERVICE_URL}/get_goods")
        goods_list = response.json()
        available_goods = [{"name": good["name"], "price": good["price"]} for good in goods_list]
        return available_goods
    except Exception as e:
        return {"error": f"Error fetching available goods: {str(e)}"}

def get_good_details(good_name):
    """
    Retrieves details of a specific good by its name from the goods service.

    Args:
        good_name (str): The name of the good.

    Returns:
        dict: A dictionary containing information about the specified good.
    """
    try:
        response = requests.get(f"{GOODS_SERVICE_URL}/get_goods")
        goods_list = response.json()
        for good in goods_list:
            if good["name"] == good_name:
                return good
        return {"error": "Good not found"}
    except Exception as e:
        return {"error": f"Error fetching good details: {str(e)}"}

def save_purchase_history(purchase_history):
    """
    Saves the purchase history to the purchase history table.

    Args:
        purchase_history (dict): A dictionary containing information about the purchase.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO purchase_history (customer_username, good_name, good_price, timestamp) VALUES (?, ?, ?, ?)",
                    (purchase_history['customer_username'], purchase_history['good_name'], purchase_history['good_price'], purchase_history['timestamp']))
        conn.commit()
    except Exception as e:
        print(f"Error saving purchase history: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

def get_full_purchase_history():
    """
    Retrieves the full purchase history from the purchase history table.

    Returns:
        list: A list of dictionaries containing information about each purchase.
    """
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM purchase_history")
        rows = cur.fetchall()
        purchase_history_list = [dict(row) for row in rows]
        return purchase_history_list
    except Exception as e:
        print(f"Error fetching full purchase history: {str(e)}")
        return {"error": "Error fetching full purchase history"}
    finally:
        conn.close()

def get_user_purchase_history(customer_username):
    """
    Retrieves the purchase history of a specific user from the purchase history table.

    Args:
        customer_username (str): The username of the customer.

    Returns:
        list: A list of dictionaries containing information about each purchase of the user.
    """
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM purchase_history WHERE customer_username = ?", (customer_username,))
        rows = cur.fetchall()
        user_purchase_history = [dict(row) for row in rows]
        return user_purchase_history
    except Exception as e:
        print(f"Error fetching user purchase history: {str(e)}")
        return {"error": "Error fetching user purchase history"}
    finally:
        conn.close()

def make_sale(good_name, customer_username):
    """
    Processes a sale, deducting money from the customer's wallet, updating the goods count, and saving the purchase history.

    Args:
        good_name (str): The name of the good to be purchased.
        customer_username (str): The username of the customer making the purchase.

    Returns:
        dict: A dictionary containing a status message or an error message if the sale process fails.
    """
    try:
        # Check if the good is available
        good_details = get_good_details(good_name)
        if "error" in good_details:
            return good_details

        # Check if the customer has enough money
        customer_details = requests.get(f"{CUSTOMER_SERVICE_URL}/get_customer/{customer_username}").json()
        if "error" in customer_details:
            return customer_details

        good_price = good_details["price"]
        customer_wallet_balance = customer_details["wallet_balance"]

        if customer_wallet_balance < good_price:
            return {"error": "Insufficient funds to make the purchase"}

        # Deduct money from customer's wallet
        response_deduct = requests.put(f"{CUSTOMER_SERVICE_URL}/deduct_wallet/{customer_username}/{good_price}")
        if response_deduct.status_code != 200:
            return {"error": "Error deducting money from customer's wallet"}

        # Update the count of the purchased good
        updated_goods = {
            "id": good_details["id"],
            "name": good_details["name"],
            "category": good_details["category"],
            "price": good_details["price"],
            "description": good_details["description"],
            "count": good_details["count"] - 1  # Assuming 1 item per purchase
        }
        response_update_goods = requests.put(f"{GOODS_SERVICE_URL}/update_goods", json=updated_goods)
        if response_update_goods.status_code != 200:
            # Rollback the deducted money
            requests.put(f"{CUSTOMER_SERVICE_URL}/charge_wallet/{customer_username}/{good_price}")
            return {"error": "Error updating goods count"}

        # Save the purchase history
        purchase_history = {
            "customer_username": customer_username,
            "good_name": good_name,
            "good_price": good_price,
            "timestamp": "current_timestamp()"  # could have used datetime but decided to just comment it out for now
        }
        save_purchase_history(purchase_history)

        return {"status": "Sale completed successfully"}
    except Exception as e:
        return {"error": f"Error making sale: {str(e)}"}