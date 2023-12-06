# Example configuration settings for Service 2 (Inventory)

# Flask app configuration
DEBUG = True
SECRET_KEY = 'your_secret_key'

# Database configuration
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost:5432/service2_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Inventory-related configuration
MAX_STOCK_COUNT = 1000  # Example maximum count for available items in stock

# Add any other service-specific configurations
