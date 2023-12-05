# Example configuration settings for Service 3 (Sales)

# Flask app configuration
DEBUG = True
SECRET_KEY = 'your_secret_key'

# Database configuration
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost:5432/service3_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Sale-related configuration
SALES_HISTORY_ENABLED = True  # Example: Enable or disable saving historical purchases

# Add any other service-specific configurations
