from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)
CSV_FILE = 'licenses.csv'


def read_licenses():
    licenses = {}
    if not os.path.exists(CSV_FILE):
        return licenses
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            licenses[row['software']] = row['license']
    return licenses


def write_license(software, license_text):
    licenses = read_licenses()
    licenses[software] = license_text
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['software', 'license']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for sw, lic in licenses.items():
            writer.writerow({'software': sw, 'license': lic})


@app.route('/')
def index():
    return 'Hello, this is version `1.0.0` of your flask app'


@app.route('/licenses', methods=['GET'])
def get_licenses():
    licenses = read_licenses()
    return jsonify(licenses), 200


@app.route('/licenses/<software>', methods=['GET'])
def get_license(software):
    licenses = read_licenses()
    if software in licenses:
        return jsonify({software: licenses[software]}), 200
    return jsonify({'error': 'Software not found'}), 404


@app.route('/licenses', methods=['POST'])
def add_license():
    data = request.get_json()
    if not data or 'software' not in data or 'license' not in data:
        return jsonify({'error': 'Invalid input, expected JSON with "software" and "license" fields'}), 400

    software = data['software']
    license_text = data['license']
    write_license(software, license_text)

    return jsonify({'message': f'License for {software} added/updated'}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
