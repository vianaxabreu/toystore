from flask import Flask, request, jsonify
from support.my_sheet import MyGsheet
import toml
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# get credentials
config = toml.load(".env.toml")
CRED = config["google_credentials"]
SHEET_ID = config["sheet_id"]["sheet_id"]
range_name = "Form!A2:E5"

ms = MyGsheet(cred=CRED)
ms.initialize_service()

@app.route('/submit', methods=['POST', 'OPTIONS'])
def submit():
    if request.method == 'OPTIONS':
        # Respond to preflight requests
        return jsonify({"status": "ok"}), 200 # Add status code 200
    data = request.get_json()
    # id    full_name   email   order_number    message
    values = [[
        data.get("id"),
        data.get("full_name"),
        data.get("email"),
        data.get("order_number"),
        data.get("message")
    ]]

    body = {"values": values}

    ms.service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=range_name,
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()

    return jsonify({"status": "success"})


@app.route('/')
def hello_world():
    return {"hello": "world"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)