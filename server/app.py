from flask import Flask, request
import json
import os

app = Flask(__name__, static_folder='../public', static_url_path='')

DATA_FILE = 'server/data.json'

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()

    if not all(k in data for k in ['name', 'age', 'occupation']):
        return "Missing fields", 400

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)

    with open(DATA_FILE, 'r+') as f:
        existing = json.load(f)
        existing.append(data)
        f.seek(0)
        json.dump(existing, f, indent=2)

    return "Information saved successfully!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
