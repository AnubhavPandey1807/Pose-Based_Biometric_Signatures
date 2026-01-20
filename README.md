# Vision-Based Pose Biometric Authentication System

## Overview
This project implements a **multi-factor authentication system** that combines:
- Traditional credentials (username + password)
- **Vision-based behavioral biometrics** using human pose signatures
- **Temporal liveness detection** to prevent replay and spoofing attacks

The system uses real-time webcam input and MediaPipe Pose estimation to extract
pose landmarks and generate a **pose signature** unique to each user.

---

## Key Features
- 🔐 Username + password authentication
- 🧍 Pose-based biometric verification
- 🎥 Real-time webcam capture via browser
- 🧠 Liveness detection using temporal variance
- 🛡️ Spoof-resistant (no static image/video replay)
- 🌐 Web-based interface using FastAPI + HTML/CSS/JS

---

## Technology Stack

### Backend
- **FastAPI** – REST API and server-side rendering
- **SQLAlchemy** – ORM with SQLite database
- **MediaPipe Pose** – Human pose landmark detection
- **OpenCV** – Image processing
- **NumPy / SciPy** – Mathematical computations
- **Passlib (bcrypt)** – Secure password hashing

### Frontend
- HTML5
- CSS3 (custom dark-classified UI)
- Vanilla JavaScript
- WebRTC (`getUserMedia`) for webcam access

---

## Project Structure

POSE_ESTIMATOR_PROJECT/
│
├── app/
│ ├── api/ # Authentication routes
│ ├── core/ # Pose logic, security, liveness
│ ├── db/ # Database models and session
│ ├── static/ # CSS & JS
│ ├── templates/ # HTML pages
│ └── main.py # FastAPI entry point
│
├── pose_detector.py # MediaPipe pose extraction
├── pose_landmarker_lite.task
├── requirements.txt
└── README.md



---

## Authentication Flow

### Registration
1. User enters username and password
2. Webcam records multiple pose frames
3. Pose landmarks are extracted
4. A **pose signature vector** is computed
5. Signature + hashed password are stored

### Login
1. User provides credentials
2. Live pose is captured
3. New pose signature is generated
4. System compares stored vs live signature
5. Liveness check ensures real movement
6. Access granted only if all checks pass

---

## Liveness Detection Logic
The system verifies:
- **Total pose movement** over time
- **Temporal variance** across pose vectors

This prevents:
- Static image attacks
- Pre-recorded video replays
- Screenshot spoofing

---

## Installation & Setup

### 1. Create Virtual Environment
```bash
py -3.12 -m venv pose_env 
pose_env\Scripts\activate
