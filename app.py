from flask import (
    Flask,
    render_template,
    Response,
    request,
    redirect,
    url_for,
    jsonify,
    send_from_directory
)
import os
import json

from engines.violence_engine import ViolenceEngine
from engines.face_engine import FaceEngine

# ==================================================
# APP INITIALIZATION
# ==================================================
app = Flask(__name__)

os.makedirs("uploads", exist_ok=True)
os.makedirs("alerts", exist_ok=True)
os.makedirs("faces", exist_ok=True)
os.makedirs("faces/known", exist_ok=True)

# ==================================================
# ENGINES
# ==================================================
violence_engine = ViolenceEngine()
face_engine = FaceEngine()

current_engine = "violence"

# Start violence engine by default
violence_engine.start(0)

# ==================================================
# STREAM GENERATOR
# ==================================================
def generate_stream(engine):
    for frame in engine.frames():
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            frame +
            b"\r\n"
        )

# ==================================================
# ROUTES – PAGES
# ==================================================
@app.route("/")
def home():
    return render_template("page1_home.html")


@app.route("/identify")
def identify():
    global current_engine

    if current_engine != "face":
        violence_engine.stop()
        face_engine.start(0)
        current_engine = "face"

    return render_template("page3_identify.html")


@app.route("/page2")
def page2():
    return render_template("page2_upload.html")

# ==================================================
# ROUTES – VIDEO STREAMS
# ==================================================
@app.route("/video_feed")
def video_feed():
    global current_engine

    if current_engine != "violence":
        face_engine.stop()
        violence_engine.start(0)
        current_engine = "violence"

    return Response(
        generate_stream(violence_engine),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/face_feed")
def face_feed():
    global current_engine

    if current_engine != "face":
        violence_engine.stop()
        face_engine.start(0)
        current_engine = "face"

    return Response(
        generate_stream(face_engine),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

# ==================================================
# ROUTES – ALERT DATA
# ==================================================
@app.route("/alerts")
def get_alerts():
    log_path = "alerts/log.json"
    if not os.path.exists(log_path):
        return jsonify([])
    with open(log_path, "r") as f:
        return jsonify(json.load(f))


@app.route("/alerts/<path:filename>")
def serve_alert_image(filename):
    return send_from_directory("alerts", filename)

# ==================================================
# ROUTES – VIDEO UPLOAD
# ==================================================
@app.route("/upload_video", methods=["POST"])
def upload_video():
    global current_engine

    if "video" not in request.files:
        return ("No file uploaded", 400)

    file = request.files["video"]
    if file.filename == "":
        return ("Empty filename", 400)

    video_path = "uploads/temp_video.mp4"
    file.save(video_path)

    if current_engine == "violence":
        violence_engine.stop()
        violence_engine.start(video_path)
    else:
        face_engine.stop()
        face_engine.start(video_path)

    return ("", 204)

# ==================================================
# ✅ FACE ENROLLMENT ROUTE (THIS FIXES 404)
# ==================================================
@app.route("/enroll_face", methods=["POST"])
def enroll_face():
    name = request.form.get("person_name", "").strip()
    images = request.files.getlist("images")

    if not name or not images:
        return "Invalid input", 400

    person_dir = os.path.join("faces", "known", name)
    os.makedirs(person_dir, exist_ok=True)

    for img in images:
        img.save(os.path.join(person_dir, img.filename))

    print(f"[INFO] Enrolled person: {name} ({len(images)} images)")

    # Reload faces immediately
    face_engine.load_known_faces()

    return redirect(url_for("identify"))

# ==================================================
# ROUTE – SWITCH BACK TO HOME
# ==================================================
@app.route("/switch_to_home")
def switch_to_home():
    global current_engine

    if current_engine != "violence":
        face_engine.stop()
        violence_engine.start(0)
        current_engine = "violence"

    return redirect(url_for("home"))

# ==================================================
# MAIN
# ==================================================
if __name__ == "__main__":
    app.run(debug=True)
