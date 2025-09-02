from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__, static_folder='../public', static_url_path='')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data.json')
print("Received data:", data)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()

    if not all(k in data for k in ['name', 'age', 'occupation']):
        return "Missing fields", 400

    # Make sure file exists
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)

    with open(DATA_FILE, 'r+') as f:
        try:
            existing = json.load(f)
        except json.JSONDecodeError:
            existing = []
        existing.append(data)
        f.seek(0)
        f.truncate()
        json.dump(existing, f, indent=2)

    return "Information saved successfully!"
