import requests
import sqlite3

# Fungsi untuk mengirim data API
def send_data_to_api(body):
    url = 'http://127.0.0.1:5000/api/simulate'
    headers = {
        'x-ca-key': 'x-ca-key',
        'x-ca-signature': 'x-ca-signature',
        'x-ca-signature-headers': 'x-ca-signature-headers'
    }
    response = requests.post(url, json=body, headers=headers)
    return response.json()

# Fungsi untuk menyimpan data ke dalam database SQLite
def save_to_database(data):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS person (
                        personId INTEGER PRIMARY KEY,
                        personCode TEXT,
                        personName TEXT,
                        personFamilyName TEXT,
                        personGivenName TEXT
                    )''')
    conn.commit()

    person_id = data['data']['personId']
    person_code = data['data']['personCode']
    person_name = data['data']['personName']
    person_family_name = data['data']['personFamilyName']
    person_given_name = data['data']['personGivenName']

    cursor.execute('''INSERT INTO person (personId, personCode, personName, personFamilyName, personGivenName)
                      VALUES (?, ?, ?, ?, ?)''',
                   (person_id, person_code, person_name, person_family_name, person_given_name))
    conn.commit()
    conn.close()

# Fungsi untuk mengambil data dari API dan menyimpan ke dalam database SQLite
def main():
    person_code = input("Masukkan PersonCode: ")
    body_sample = {
        "personCode": person_code
    }
    api_response = send_data_to_api(body_sample)
    if api_response['code'] == '0' and api_response['msg'] == 'Success':
        save_to_database(api_response)
        print("Data berhasil disimpan ke dalam database.")
    else:
        print("Gagal mengirim data atau menyimpan ke database.")

if __name__ == "__main__":
    main()