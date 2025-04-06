from flask import Flask, render_template
import os
import socket

app = Flask(__name__)

@app.route("/")
def index():
    image_folder = os.path.join("static", "images")
    images = os.listdir(image_folder)
    images = [img for img in images if img.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))]
    return render_template("index.html", images=images)

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
    print(f"\n🟢 Flask-appen körs på:")
    print(f"   http://{ip}:5000  ← öppna denna i din mobil\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
