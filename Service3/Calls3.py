from flask import Flask, request, jsonify
from Doc_Ser3 import *

app = Flask(__name__)

@app.route('/display_available_goods', methods=['GET'])
def display_available_goods_route():
    available_goods = display_available_goods()
    return jsonify(available_goods)

@app.route('/get_good_details/<good_name>', methods=['GET'])
def get_good_details_route(good_name):
    good_details = get_good_details(good_name)
    return jsonify(good_details)

@app.route('/make_sale', methods=['POST'])
def make_sale_route():
    data = request.get_json()
    result = make_sale(data['good_name'], data['customer_username'])
    return jsonify(result)

@app.route('/full_purchase_history', methods=['GET'])
def full_purchase_history_route():
    full_purchase_history = get_full_purchase_history()
    return jsonify(full_purchase_history)

@app.route('/user_purchase_history/<customer_username>', methods=['GET'])
def user_purchase_history_route(customer_username):
    user_purchase_history = get_user_purchase_history(customer_username)
    return jsonify(user_purchase_history)

if __name__ == '__main__':
    app.run(debug=True, port=5003)
