# Example configuration settings for Service 1 (Customers)

# Flask app configuration
DEBUG = True
SECRET_KEY = 'your_secret_key'

# Database configuration
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost:5432/service1_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Customer-related configuration
CUSTOMER_WALLET_INITIAL_BALANCE = 100.0  # Example initial balance for customer wallets

# Add any other service-specific configurations
