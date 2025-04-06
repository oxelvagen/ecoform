from flask import Flask, render_template, request, redirect, session, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "superhemligt123"  # För sessionshantering
UPLOAD_PASSWORD = "Flaskhals!"

@app.route("/", methods=["GET", "POST"])
def index():
    image_folder = os.path.join("static", "images")
    images = os.listdir(image_folder)
    images = [img for img in images if img.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        return render_template("index.html", images=images, success=True)

    return render_template("index.html", images=images)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if session.get("auth") != True:
        return redirect("/login")

    image_folder = os.path.join("static", "images")
    if request.method == "POST":
        files = request.files.getlist("images")
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
    if session.get("auth") != True:
        return redirect("/login")

    image_folder = os.path.join("static", "images")
    images = os.listdir(image_folder)
    images = [img for img in images if img.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
    return render_template("admin.html", images=images)

@app.route("/delete", methods=["POST"])
def delete_image():
    if session.get("auth") != True:
        return redirect("/login")

    image = request.form.get("image")
    path = os.path.join("static", "images", image)
    if os.path.exists(path):
        os.remove(path)
    return redirect("/admin")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == UPLOAD_PASSWORD:
            session["auth"] = True
            return redirect("/admin")
        else:
            return "<h3>Fel lösenord</h3>"
    return '''
        <form method="POST">
            <input type="password" name="password" placeholder="Lösenord">
            <button type="submit">Logga in</button>
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
