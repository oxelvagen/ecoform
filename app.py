from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_PASSWORD = "eco123"

@app.route("/", methods=["GET"])
def index():
    image_folder = os.path.join("static", "images")
    images = os.listdir(image_folder)
    images = [img for img in images if img.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
    return render_template("index.html", images=images)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    image_folder = os.path.join("static", "images")
    if request.method == "POST":
        password = request.form.get("password")
        files = request.files.getlist("images")
        if password != UPLOAD_PASSWORD:
            return render_template("upload.html", message="Fel lösenord", success=False)

        saved = 0
        for file in files:
            if file.filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                filename = secure_filename(file.filename)
                file.save(os.path.join(image_folder, filename))
                saved += 1

        return render_template("upload.html", message=f"{saved} bild(er) uppladdade!", success=True)

    return render_template("upload.html")

@app.route("/admin", methods=["GET"])
def admin():
    image_folder = os.path.join("static", "images")
    images = os.listdir(image_folder)
    images = [img for img in images if img.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
    return render_template("admin.html", images=images)

@app.route("/delete", methods=["POST"])
def delete_image():
    image = request.form.get("image")
    path = os.path.join("static", "images", image)
    if os.path.exists(path):
        os.remove(path)
    return redirect("/admin")

if __name__ == "__main__":
    app.run(debug=True)
