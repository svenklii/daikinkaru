from flask import Flask, request, redirect, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Get Daikin API URL and API Key from environment variables
DAIKIN_API_URL = os.getenv("DAIKIN_API_URL")
DAIKIN_API_KEY = os.getenv("DAIKIN_API_KEY")

# Endpoint to get Daikin device status
@app.route('/device_status', methods=['GET'])
def get_device_status():
    try:
        # Make a GET request to Daikin API
        response = requests.get(
            f"{DAIKIN_API_URL}/status",
            headers={"Authorization": f"Bearer {DAIKIN_API_KEY}"}
        )
        
        # If the response is successful, return the status
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": "Failed to fetch device status"}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to control Daikin device (e.g., turn on or off)
@app.route('/control_device', methods=['POST'])
def control_device():
    try:
        # Get the command and device ID from the POST request body
        data = request.json
        device_id = data.get("device_id")
        action = data.get("action")  # Example: "turn_on" or "turn_off"

        # Make a POST request to Daikin API to control the device
        payload = {"device_id": device_id, "action": action}
        response = requests.post(
            f"{DAIKIN_API_URL}/control",
            json=payload,
            headers={"Authorization": f"Bearer {DAIKIN_API_KEY}"}
        )

        # If the response is successful, return the result
        if response.status_code == 200:
            return jsonify({"message": "Device control successful"}), 200
        else:
            return jsonify({"error": "Failed to control device"}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
