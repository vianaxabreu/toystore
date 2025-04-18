from flask import Flask, request, jsonify
from support.my_sheet import MyGsheet
import toml
from flask_cors import CORS
from google.auth import default
import os # used if in cloud run

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# get credentials
# config = toml.load(".env.toml") not required if cloud run
# CRED = config["google_credentials"]
# SHEET_ID = config["sheet_id"]["sheet_id"]

CRED, _ = default()
SHEET_ID = os.getenv("sheet_id")

ms = MyGsheet(cred=CRED)
ms.initialize_service()

@app.route('/submit_form', methods=['POST', 'OPTIONS'])
def submit():
    range_name = "Form!A2:E5"
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

@app.route('/submit_order', methods=['POST', 'OPTIONS'])
def submit_order():
    range_name = "Order!A2:E5"
    if request.method == 'OPTIONS':
        # Respond to preflight requests
        return jsonify({"status": "ok"}), 200 # Add status code 200
    data = request.get_json()
    # id	full_name	order_number	total_price	total_quantity items
    values = [[
        data.get("id"),
        data.get("full_name"),
        data.get("order_number"),
        data.get("total_price"),
        data.get("total_quantity"),
        data.get("items")
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
    # app.run(host='0.0.0.0', port=5002)
    app.run(host='0.0.0.0', port=8080)