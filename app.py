from flask import Flask, render_template, request, redirect
import os
import socket
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    image_folder = os.path.join("static", "images")
    images = os.listdir(image_folder)
    images = [img for img in images if img.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # Skicka e-post
        send_email(name, email, message)
        return render_template("index.html", images=images, success=True)

    return render_template("index.html", images=images)

def send_email(name, email, message):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "oxelvagen4@gmail.com"
    smtp_password = "ehev mebk jmys dclj"  # App-lösenord från Gmail

    msg = MIMEText(f"Namn: {name}\nE-post: {email}\n\nMeddelande:\n{message}")
    msg["Subject"] = "Nytt meddelande från EcoForm Portfolio"
    msg["From"] = smtp_user
    msg["To"] = smtp_user

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, smtp_user, msg.as_string())
            print("Meddelandet skickades!")
    except Exception as e:
        print("Fel vid e-post:", e)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

if __name__ == "__main__":
    ip = get_local_ip()
    print(f"\n🟢 Öppna i mobilen: http://{ip}:5000\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
