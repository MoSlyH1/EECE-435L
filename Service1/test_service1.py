import pytest
import requests

# Define the base URL for the Flask app
BASE_URL = 'http://127.0.0.1:5001'

# Define test functions for each endpoint in app.py

def test_register_customer():
    """
    Test the /register_customer endpoint.

    Asserts that the status code of the response is 200.
    """
    response = requests.post(f'{BASE_URL}/register_customer', json={   
    "full_name": "Monkey D. Luffy",
    "username": "kingofthepirates",
    "password": "theonepiece",
    "age": 19,
    "address": "East Blue",
    "gender": "Male",
    "marital_status": "Single"})
    assert response.status_code == 200

def test_get_customers_route():
    """
    Test the /get_customers endpoint.

    Asserts that the status code of the response is 200.
    """
    response = requests.get(f'{BASE_URL}/get_customers')
    assert response.status_code == 200

def test_get_customer_by_username_route():
    """
    Test the /get_customer/<username> endpoint.

    Asserts that the status code of the response is 200.
    """
    response = requests.get(f'{BASE_URL}/get_customer/username')
    assert response.status_code == 200

def test_update_customer_route():
    """
    Test the /update_customer endpoint.

    Asserts that the status code of the response is 200.
    """
    response = requests.put(f'{BASE_URL}/update_customer', json={
    "address": "Grand Line",
    "age": 19,
    "full_name": "Monkey D. Luffy",
    "gender": "Male",
    "id": 3,
    "marital_status": "Single",
    "password": "theonepiece",
    "username": "kingofthepirates",
    "wallet_balance": 0.0
})
    assert response.status_code == 200

def test_delete_customer_route():
    """
    Test the /delete_customer/<int:customer_id> endpoint.

    Asserts that the status code of the response is 200.
    """
    response = requests.delete(f'{BASE_URL}/delete_customer/4')
    assert response.status_code == 200

def test_charge_wallet_route():
    """
    Test the /charge_wallet/<username>/<float:amount> endpoint.

    Asserts that the status code of the response is 200.
    """
    response = requests.put(f'{BASE_URL}/charge_wallet/username/100.0')
    assert response.status_code == 200

def test_deduct_wallet_route():
    """
    Test the /deduct_wallet/<username>/<float:amount> endpoint.

    Asserts that the status code of the response is 200.
    """
    response = requests.put(f'{BASE_URL}/deduct_wallet/username/50.0')
    assert response.status_code == 200

# Run the tests

if __name__ == '__main__':
    pytest.main(['-v', 'test_service1.py'])