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

if __name__ == '__main__':
    app.run(debug=True, port=5003)
