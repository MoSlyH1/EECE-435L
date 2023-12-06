from flask import Flask, request, jsonify
from Doc_Ser2 import *

app = Flask(__name__)

@app.route('/add_goods', methods=['POST'])
def add_goods():
    data = request.get_json()
    goods = insert_goods(data)
    return jsonify(goods)

@app.route('/deduct_goods/<int:goods_id>', methods=['DELETE'])
def deduct_goods_route(goods_id):
    message = deduct_goods(goods_id)
    return jsonify(message)

@app.route('/update_goods', methods=['PUT'])
def update_goods_route():
    data = request.get_json()
    updated_goods = update_goods(data)
    return jsonify(updated_goods)

@app.route('/get_goods', methods=['GET'])
def get_goods_route():
    goods_list = get_goods()
    return jsonify(goods_list)

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Adjust the port as needed
