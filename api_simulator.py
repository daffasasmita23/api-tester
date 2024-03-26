from flask import Flask, request, jsonify

app = Flask(__name__)

# Data simulasi yang akan dikembalikan oleh API
simulated_data = {
    "20012": {
        "personId": "1",
        "personCode": "20012",
        "personName": "Roronoa Zoro",
        "personFamilyName": "FamilyName",
        "personGivenName": "GivenName"
    }
}

# Endpoint untuk menerima permintaan POST
@app.route('/api/simulate', methods=['POST'])
def simulate_api():
    # Mendapatkan header
    x_ca_key = request.headers.get('x-ca-key')
    x_ca_signature = request.headers.get('x-ca-signature')
    x_ca_signature_headers = request.headers.get('x-ca-signature-headers')

    # Mendapatkan data dari body request
    data = request.get_json()
    person_code = data.get('personCode', None)

    # Memeriksa apakah personCode ada dalam data simulasi
    if person_code in simulated_data:
        response_data = {
            "code": "0",
            "msg": "Success",
            "data": simulated_data[person_code]
        }
    else:
        response_data = {
            "code": "-1",
            "msg": "PersonCode not found"
        }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)