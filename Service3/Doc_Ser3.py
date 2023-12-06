
import requests
import sqlite3


# URLs for the customer and goods services
CUSTOMER_SERVICE_URL = "http://localhost:5001"  # Update with the actual URL of the customer service
GOODS_SERVICE_URL = "http://localhost:5002"     # Update with the actual URL of the goods service

# Database setup
def connect_to_db():
    conn = sqlite3.connect('purchase_history.db')
    return conn

def create_purchase_history_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE purchase_history (
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
    try:
        response = requests.get(f"{GOODS_SERVICE_URL}/get_goods")
        goods_list = response.json()
        available_goods = [{"name": good["name"], "price": good["price"]} for good in goods_list]
        return available_goods
    except Exception as e:
        return {"error": f"Error fetching available goods: {str(e)}"}

def get_good_details(good_name):
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

def make_sale(good_name, customer_username):
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

        # Deduct the count of the purchased good
        response_deduct_goods = requests.put(f"{GOODS_SERVICE_URL}/deduct_goods/{good_details['id']}/1")
        if response_deduct_goods.status_code != 200:
            # Rollback the deducted money
            requests.put(f"{CUSTOMER_SERVICE_URL}/charge_wallet/{customer_username}/{good_price}")
            return {"error": "Error deducting goods count"}

        # Save the purchase history
        purchase_history = {
            "customer_username": customer_username,
            "good_name": good_name,
            "good_price": good_price,
            "timestamp": "current_timestamp()"  # You may use a library like datetime to get the actual timestamp
        }
        save_purchase_history(purchase_history)

        return {"status": "Sale completed successfully"}
    except Exception as e:
        return {"error": f"Error making sale: {str(e)}"}