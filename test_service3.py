import pytest
import requests

# Define the base URL for the Flask app
BASE_URL_CUSTOMER = 'http://127.0.0.1:5001'
BASE_URL_SERVICE3 = 'http://127.0.0.1:5003'

# Define test functions for each endpoint in app.py

def get_customer_wallet_balance(username):
    """
    Helper function to get the wallet balance of a customer.
    """
    response = requests.get(f'{BASE_URL_CUSTOMER}/get_customer/{username}')
    return response.json().get('wallet_balance', 0.0)

def get_good_price(good_name):
    """
    Helper function to get the price of a good.
    """
    response = requests.get(f'{BASE_URL_SERVICE3}/get_good_details/{good_name}')
    good_details = response.json()
    return good_details.get('price', 0.0)

def test_display_available_goods_route():
    """
    Test the /display_available_goods endpoint.

    Asserts that the status code of the response is 200.
    """
    response = requests.get(f'{BASE_URL_SERVICE3}/display_available_goods')
    assert response.status_code == 200

def test_get_good_details_route():
    """
    Test the /get_good_details/<good_name> endpoint.

    Asserts that the status code of the response is 200.
    """
    response = requests.get(f'{BASE_URL_SERVICE3}/get_good_details/Laptop')
    assert response.status_code == 200

def test_make_sale_route():
    """
    Test the /make_sale endpoint.

    Asserts that the status code of the response is 200 and checks if the correct amount is deducted.
    """
    # Get the user's wallet balance before the purchase
    initial_wallet_balance = get_customer_wallet_balance("hemag")

    # Get the good's details
    good_details_response = requests.get(f'{BASE_URL_SERVICE3}/get_good_details/laptop')
    good_details = good_details_response.json()

    # Extract the price from the good details
    good_price = good_details.get('price', 0.0)

    # Make the purchase
    response = requests.post(f'{BASE_URL_SERVICE3}/make_sale', json={
        "customer_username": "hemag",
        "good_name": "laptop"
    })
    assert response.status_code == 200

    # Get the user's wallet balance after the purchase
    final_wallet_balance = get_customer_wallet_balance("hemag")

    # Check if the correct amount is deducted
    assert final_wallet_balance == (initial_wallet_balance - good_price)

def test_full_purchase_history_route():
    """
    Test the /full_purchase_history endpoint.

    Asserts that the status code of the response is 200.
    """
    response = requests.get(f'{BASE_URL_SERVICE3}/full_purchase_history')
    assert response.status_code == 200

def test_user_purchase_history_route():
    """
    Test the /user_purchase_history/<customer_username> endpoint.

    Asserts that the status code of the response is 200.
    """
    response = requests.get(f'{BASE_URL_SERVICE3}/user_purchase_history/hemag')
    assert response.status_code == 200

# Run the tests

if __name__ == '__main__':
    pytest.main(['-v', 'test_service3.py'])
