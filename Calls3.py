from flask import Flask, request, jsonify
from Doc_Ser3 import *

app = Flask(__name__)

@app.route('/display_available_goods', methods=['GET'])
def display_available_goods_route():
    """
    Endpoint for displaying available goods.

    Returns:
        jsonify: A JSON response containing a list of available goods or an error message.
    """
    available_goods = display_available_goods()
    return jsonify(available_goods)

@app.route('/get_good_details/<good_name>', methods=['GET'])
def get_good_details_route(good_name):
    """
    Endpoint for retrieving details of a specific good by its name.

    Args:
        good_name (str): The name of the good.

    Returns:
        jsonify: A JSON response containing details of the specified good or an error message.
    """
    good_details = get_good_details(good_name)
    return jsonify(good_details)

@app.route('/make_sale', methods=['POST'])
def make_sale_route():
    """
    Endpoint for processing a sale, deducting money from the customer's wallet, updating the goods count, and saving the purchase history.

    Expects a JSON payload in the request with information about the good and customer making the purchase.

    Returns:
        jsonify: A JSON response containing a status message or an error message if the sale process fails.
    """
    data = request.get_json()
    result = make_sale(data['good_name'], data['customer_username'])
    return jsonify(result)

@app.route('/full_purchase_history', methods=['GET'])
def full_purchase_history_route():
    """
    Endpoint for retrieving the full purchase history.

    Returns:
        jsonify: A JSON response containing a list of dictionaries with information about each purchase.
    """
    full_purchase_history = get_full_purchase_history()
    return jsonify(full_purchase_history)

@app.route('/user_purchase_history/<customer_username>', methods=['GET'])
def user_purchase_history_route(customer_username):
    """
    Endpoint for retrieving the purchase history of a specific user.

    Args:
        customer_username (str): The username of the customer.

    Returns:
        jsonify: A JSON response containing a list of dictionaries with information about each purchase of the user.
    """
    user_purchase_history = get_user_purchase_history(customer_username)
    return jsonify(user_purchase_history)

if __name__ == '__main__':
    app.run(debug=True, port=5003)
