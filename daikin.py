from flask import Flask, request, redirect
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
CLIENT_ID = os.getenv("DAIKIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("DAIKIN_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTH_URL = os.getenv("AUTH_URL")
TOKEN_URL = os.getenv("TOKEN_URL")
API_BASE_URL = os.getenv("API_BASE_URL")

app = Flask(__name__)

@app.route("/")
def home():
    # Redirect to Daikin's authorization URL
    auth_request_url = (
        f"{AUTH_URL}?response_type=code&client_id=1JwXzkO07DM8Mwf4KI4tjs6V"
        f"&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=read"
    )
    return redirect(auth_request_url)

@app.route("/callback")
def callback():
    # Get the authorization code from the query params
    code = request.args.get("code")
    if not code:
        return "Authorization failed", 400

    # Exchange the authorization code for an access token
    token_response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
    )
    
    token_data = token_response.json()
    access_token = token_data.get("access_token")
    if not access_token:
        return f"Token exchange failed: {token_data}", 400

    # Use the access token to call the API
    api_response = requests.get(
        f"{API_BASE_URL}/endpoint",  # Replace with the actual endpoint
        headers={"Authorization": f"Bearer {access_token}"}
    )
    return api_response.json()

if __name__ == "__main__":
    app.run(debug=True)
