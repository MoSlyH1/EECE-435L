from flask import Flask, request, jsonify
from Doc_Ser1 import *
app = Flask(__name__)


@app.route('/register_customer', methods=['POST'])
def register_customer():
    data = request.get_json()
    customer = insert_customer(data)
    return jsonify(customer)

@app.route('/get_customers', methods=['GET'])
def get_customers_route():
    customers_list = get_customers()
    return jsonify(customers_list)

@app.route('/get_customer/<username>', methods=['GET'])
def get_customer_by_username_route(username):
    customer = get_customer_by_username(username)
    return jsonify(customer)

@app.route('/update_customer', methods=['PUT'])
def update_customer_route():
    data = request.get_json()
    updated_customer = update_customer(data)
    return jsonify(updated_customer)

@app.route('/delete_customer/<int:customer_id>', methods=['DELETE'])
def delete_customer_route(customer_id):
    message = delete_customer(customer_id)
    return jsonify(message)

@app.route('/charge_wallet/<username>/<float:amount>', methods=['PUT'])
def charge_wallet_route(username, amount):
    message = charge_wallet(username, amount)
    return jsonify(message)

@app.route('/deduct_wallet/<username>/<float:amount>', methods=['PUT'])
def deduct_wallet_route(username, amount):
    message = deduct_wallet(username, amount)
    return jsonify(message)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
