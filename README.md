# Integrated Surveillance System

An AI-powered surveillance system for real-time violence detection, weapon detection, face recognition, object tracking, and Telegram-based alert generation using Computer Vision and Deep Learning.

## Features

- Violence Detection
- Weapon Detection
- Face Recognition using FaceNet
- Person Tracking
- Real-Time CCTV Video Analysis
- Telegram Alert Notifications
- YOLO-based Object Detection
- Integrated Security Monitoring System

---

## Technologies Used

### Programming Language
- Python

### Computer Vision
- OpenCV

### Deep Learning
- YOLOv8
- FaceNet
- PyTorch

### Alert System
- Telegram Bot API

### Web Framework
- Flask

---

## Project Architecture

Input Video
↓
Frame Extraction
↓
YOLO Detection
↓
Violence Detection
↓
Weapon Detection
↓
Face Recognition
↓
Person Tracking
↓
Alert Generation
↓
Telegram Notification

---

## Project Files

| File | Description |
|--------|-------------|
| app.py | Main Flask Application |
| ai_engine.py | Core AI Processing Engine |
| violence_detection.py | Violence Detection Module |
| violence_detection_with_yolo.py | YOLO-Based Violence Detection |
| violence_detection_with_face.py | Face Recognition Integration |
| final_violence_weapon_system.py | Complete Surveillance Pipeline |
| tracker.py | Person Tracking Module |
| telegram_alert.py | Telegram Alert System |
| encode_known_faces_facenet.py | Face Encoding Generation |
| test_facenet.py | FaceNet Testing |
| requirements.txt | Project Dependencies |

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/Integrated-Surveillance-System.git
```

Move into project directory:

```bash
cd Integrated-Surveillance-System
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

```bash
python app.py
```

or

```bash
python final_violence_weapon_system.py
```

---

## Applications

- Smart City Surveillance
- Public Area Monitoring
- Crime Prevention Systems
- Railway Station Monitoring
- Airport Security
- Shopping Mall Security
- University Campus Surveillance

---

## Future Enhancements

- Crowd Behaviour Analysis
- Suspicious Activity Detection
- Missing Person Identification
- Multi-Camera Tracking
- Cloud-Based Surveillance Dashboard
- Real-Time Analytics Dashboard

---

## Note

Due to GitHub file size limitations, trained model weights (.pt) and sample videos are not included in this repository. Place the required model files in the project root directory before running the application.

---

## Author

**Aghosh K K**

B.Tech Computer Science and Engineering

Vimal Jyothi Engineering College

Graduation Year: 2026

---