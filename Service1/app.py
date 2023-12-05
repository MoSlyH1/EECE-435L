from flask import Flask, request, jsonify

app = Flask(__name__)

# Your customer-related routes go here

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Adjust the port as needed
