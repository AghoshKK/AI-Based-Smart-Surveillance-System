# ai_engine.py
import cv2
import time
import os
import numpy as np
import torch
import threading
import requests
from ultralytics import YOLO
from facenet_pytorch import MTCNN, InceptionResnetV1

# ================= TELEGRAM =================
BOT_TOKEN = "8393591405:AAHCnQ34YBthyAJHFgI6333L0fpqFvKyEmA"
CHAT_ID = "1548646865"

def send_telegram(msg, img=None):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=5
        )
        if img:
            with open(img, "rb") as f:
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                    data={"chat_id": CHAT_ID},
                    files={"photo": f},
                    timeout=5
                )
    except:
        pass

# ================= LOAD MODELS =================
person_model = YOLO("yolov8n.pt")
weapon_model = YOLO("best_weapon.pt")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
mtcnn = MTCNN(keep_all=False, device=device)
resnet = InceptionResnetV1(pretrained="vggface2").eval().to(device)

# ================= LOAD FACES =================
known_embs, known_names = [], []
if os.path.exists("faces/known_facenet.pkl"):
    import pickle
    data = pickle.load(open("faces/known_facenet.pkl", "rb"))
    known_embs = data["embeddings"]
    known_names = data["names"]

# ================= GLOBAL STATE =================
camera = None
current_mode = "violence"   # or "face"
current_source = 0
last_alert = {}

def start_camera(src=0):
    global camera, current_source
    if camera:
        camera.release()
    current_source = src
    camera = cv2.VideoCapture(src)

def generate_frames():
    global last_alert

    while True:
        if not camera:
            time.sleep(0.1)
            continue

        ret, frame = camera.read()
        if not ret:
            start_camera(0)
            continue

        frame = cv2.resize(frame, (800, 450))
        display = frame.copy()

        # ================= PERSON =================
        persons = person_model(frame, conf=0.4, verbose=False)[0]

        # ================= WEAPON =================
        weapons = weapon_model(frame, conf=0.15, verbose=False)[0]

        weapon_found = False
        for box in weapons.boxes:
            cls = int(box.cls[0])
            name = weapon_model.names[cls].lower()
            if name in ["gun", "knife", "weapon"]:
                weapon_found = True
                x1,y1,x2,y2 = map(int, box.xyxy[0])
                cv2.rectangle(display,(x1,y1),(x2,y2),(0,0,255),2)
                cv2.putText(display,name.upper(),(x1,y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)

        # ================= FACE =================
        if current_mode == "face" and known_embs:
            for box in persons.boxes:
                x1,y1,x2,y2 = map(int, box.xyxy[0])
                crop = frame[y1:y2, x1:x2]

                try:
                    from PIL import Image
                    face = mtcnn(Image.fromarray(crop))
                    if face is None: continue

                    emb = resnet(face.unsqueeze(0).to(device)).cpu().numpy()[0]
                    dists = np.linalg.norm(known_embs - emb, axis=1)
                    idx = int(np.argmin(dists))

                    if dists[idx] < 0.9:
                        name = known_names[idx]
                        cv2.putText(display,f"IDENTIFIED: {name}",
                                    (x1,y1-20),
                                    cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2)

                        if time.time() - last_alert.get(name,0) > 10:
                            last_alert[name] = time.time()
                            img = f"alerts/{name}_{int(time.time())}.jpg"
                            cv2.imwrite(img, display)
                            threading.Thread(
                                target=send_telegram,
                                args=(f"🚨 PERSON IDENTIFIED: {name}", img),
                                daemon=True
                            ).start()
                except:
                    pass

        # ================= VIOLENCE ALERT =================
        if weapon_found and time.time() - last_alert.get("weapon",0) > 10:
            last_alert["weapon"] = time.time()
            img = f"alerts/weapon_{int(time.time())}.jpg"
            cv2.imwrite(img, display)
            threading.Thread(
                target=send_telegram,
                args=("🚨 WEAPON DETECTED", img),
                daemon=True
            ).start()

        # ================= STREAM =================
        _, jpeg = cv2.imencode(".jpg", display)
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" +
               jpeg.tobytes() + b"\r\n")
