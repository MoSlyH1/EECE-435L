import pytest
import requests

# Define the base URL for the Flask app
BASE_URL = 'http://127.0.0.1:5002'

# Define test functions for each endpoint in app.py

def test_add_goods():
    """
    Test the /add_goods endpoint.

    Asserts that the status code of the response is 200.
    """
    response = requests.post(f'{BASE_URL}/add_goods', json={
    "name": "Straw Hat",
    "category": "clothes",
    "price": 3000.00,
    "description": "A straw hat, once owned by legendary pirates",
    "count": 4
})
    assert response.status_code == 200

def test_update_goods_route():
    """
    Test the /update_goods endpoint.

    Asserts that the status code of the response is 200.
    """
    response = requests.put(f'{BASE_URL}/update_goods', json={
    "category": "clothes",
    "count": 4,
    "description": "A straw hat, once owned by legendary pirates. Now owned by the king of the pirates.",
    "id": 3,
    "name": "Straw Hat",
    "price": 3000.0
})
    assert response.status_code == 200

def test_deduct_goods_route():
    """
    Test the /deduct_goods/<int:goods_id> endpoint.

    Asserts that the status code of the response is 200.
    """
    response = requests.delete(f'{BASE_URL}/deduct_goods/4')
    assert response.status_code == 200


def test_get_goods_route():
    """
    Test the /get_goods endpoint.

    Asserts that the status code of the response is 200.
    """
    response = requests.get(f'{BASE_URL}/get_goods')
    assert response.status_code == 200

# Run the tests

if __name__ == '__main__':
    pytest.main(['-v', 'test_service2.py'])