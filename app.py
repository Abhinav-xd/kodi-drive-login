from flask import Flask, redirect, request
import requests
import os

app = Flask(__name__)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")

@app.route("/")
def login():
    return redirect(
        "https://accounts.google.com/o/oauth2/v2/auth"
        "?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&scope=https://www.googleapis.com/auth/drive.readonly"
        "&access_type=offline"
        "&prompt=consent"
    )

@app.route("/oauth2callback")
def callback():
    code = request.args.get("code")
    token = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        },
    ).json()

    return f"<h3>Login successful</h3><pre>{token}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
