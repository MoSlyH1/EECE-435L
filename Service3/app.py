from flask import Flask, request, jsonify

app = Flask(__name__)

# Your sales-related routes go here

if __name__ == '__main__':
    app.run(debug=True, port=5003)  # Adjust the port as needed
