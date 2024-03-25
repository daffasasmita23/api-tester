from flask import Flask, request, jsonify, abort
import hmac
import hashlib

app = Flask(__name__)

# Sample data (you can replace this with your own data)
sample_data = {
    '1': {'name': 'Alice', 'age': 30},
    '2': {'name': 'Bob', 'age': 25}
}

# Secret key for HMAC signature
secret_key = b'my_test_secret_key'

# Function to authenticate requests based on x-ca-key and x-ca-signature headers
def authenticate(f):
    def decorated_function(*args, **kwargs):
        x_ca_key = request.headers.get('x-ca-key')
        x_ca_signature = request.headers.get('x-ca-signature')

        if not x_ca_key or not x_ca_signature:
            abort(401)  # Unauthorized

        # Calculate the expected signature
        expected_signature = hmac.new(secret_key, digestmod=hashlib.sha256)
        expected_signature.update(x_ca_key.encode('utf-8'))
        calculated_signature = expected_signature.hexdigest()

        # Compare the calculated signature with the received signature
        if calculated_signature != x_ca_signature:
            abort(401)  # Unauthorized

        return f(*args, **kwargs)
    return decorated_function

# Route to add new data with authentication
@app.route('/data', methods=['POST'])
@authenticate
def add_data():
    new_item = request.json
    sample_data[str(len(sample_data) + 1)] = new_item
    return jsonify({'message': 'Data added successfully'})

if __name__ == '__main__':
    app.run(debug=True)