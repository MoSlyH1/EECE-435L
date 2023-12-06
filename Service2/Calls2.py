from flask import Flask, request, jsonify
from Doc_Ser2 import *

app = Flask(__name__)

@app.route('/add_goods', methods=['POST'])
def add_goods():
    """
    Endpoint for adding new goods.

    Expects a JSON payload in the request with goods information.
    
    Returns:
        jsonify: A JSON response containing the inserted goods information or an empty response if an error occurs.
    """
    data = request.get_json()
    goods = insert_goods(data)
    return jsonify(goods)

@app.route('/deduct_goods/<int:goods_id>', methods=['DELETE'])
def deduct_goods_route(goods_id):
    """
    Endpoint for deducting goods by their ID.

    Args:
        goods_id (int): The ID of the goods to be deducted.

    Returns:
        jsonify: A JSON response containing a status message.
    """
    message = deduct_goods(goods_id)
    return jsonify(message)

@app.route('/update_goods', methods=['PUT'])
def update_goods_route():
    """
    Endpoint for updating goods information.

    Expects a JSON payload in the request with updated goods information.

    Returns:
        jsonify: A JSON response containing the updated goods information or an empty response if an error occurs.
    """
    data = request.get_json()
    updated_goods = update_goods(data)
    return jsonify(updated_goods)

@app.route('/get_goods', methods=['GET'])
def get_goods_route():
    """
    Endpoint for retrieving a list of all goods.

    Returns:
        jsonify: A JSON response containing a list of goods information.
    """
    goods_list = get_goods()
    return jsonify(goods_list)

if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Adjust the port as needed
