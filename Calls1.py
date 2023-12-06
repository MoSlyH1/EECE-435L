from flask import Flask, request, jsonify
from Doc_Ser1 import *

app = Flask(__name__)

@app.route('/register_customer', methods=['POST'])
def register_customer():
    """
    Endpoint for registering a new customer.

    Expects a JSON payload in the request with customer information.
    
    Returns:
        jsonify: A JSON response containing the inserted customer information or an error message.
    """
    data = request.get_json()
    customer = insert_customer(data)
    return jsonify(customer)

@app.route('/get_customers', methods=['GET'])
def get_customers_route():
    """
    Endpoint for retrieving a list of all customers.

    Returns:
        jsonify: A JSON response containing a list of customer information.
    """
    customers_list = get_customers()
    return jsonify(customers_list)

@app.route('/get_customer/<username>', methods=['GET'])
def get_customer_by_username_route(username):
    """
    Endpoint for retrieving a customer by their username.

    Args:
        username (str): The username of the customer.

    Returns:
        jsonify: A JSON response containing the customer information or an empty response if not found.
    """
    customer = get_customer_by_username(username)
    return jsonify(customer)

@app.route('/update_customer', methods=['PUT'])
def update_customer_route():
    """
    Endpoint for updating customer information.

    Expects a JSON payload in the request with updated customer information.

    Returns:
        jsonify: A JSON response containing the updated customer information or an empty response if an error occurs.
    """
    data = request.get_json()
    updated_customer = update_customer(data)
    return jsonify(updated_customer)

@app.route('/delete_customer/<int:customer_id>', methods=['DELETE'])
def delete_customer_route(customer_id):
    """
    Endpoint for deleting a customer by their ID.

    Args:
        customer_id (int): The ID of the customer to be deleted.

    Returns:
        jsonify: A JSON response containing a status message.
    """
    message = delete_customer(customer_id)
    return jsonify(message)

@app.route('/charge_wallet/<username>/<float:amount>', methods=['PUT'])
def charge_wallet_route(username, amount):
    """
    Endpoint for charging a customer's wallet.

    Args:
        username (str): The username of the customer.
        amount (float): The amount to be added to the wallet.

    Returns:
        jsonify: A JSON response containing a status message.
    """
    message = charge_wallet(username, amount)
    return jsonify(message)

@app.route('/deduct_wallet/<username>/<float:amount>', methods=['PUT'])
def deduct_wallet_route(username, amount):
    """
    Endpoint for deducting money from a customer's wallet.

    Args:
        username (str): The username of the customer.
        amount (float): The amount to be deducted from the wallet.

    Returns:
        jsonify: A JSON response containing a status message.
    """
    message = deduct_wallet(username, amount)
    return jsonify(message)

if __name__ == '__main__':
    app.run(debug=True, port=5001)