from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import numpy as np

from app.core.pose_service import detect_pose_signature, check_liveness
from app.core.security import hash_password, verify_password
from app.db.database import SessionLocal
from app.db.models import User

router = APIRouter()

@router.post("/register")
async def register(
    username: str = Form(...),
    password: str = Form(...),
    frames: list[UploadFile] = File(...)
):
    signatures = detect_pose_signature(frames)

    if not check_liveness(signatures):
        raise HTTPException(400, "Liveness check failed")

    pose_signature = signatures.mean(axis=0).tolist()
    password_hash = hash_password(password)

    db = SessionLocal()
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(409, "User already exists")

    user = User(
        username=username,
        password_hash=password_hash,
        pose_signature=pose_signature
    )
    db.add(user)
    db.commit()

    return {"status": "registered"}

@router.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    frames: list[UploadFile] = File(...)
):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(404, "User not found")

    if not verify_password(password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    signatures = detect_pose_signature(frames)

    if not check_liveness(signatures):
        raise HTTPException(403, "Liveness failed")

    incoming = signatures.mean(axis=0)
    stored = np.array(user.pose_signature)

    distance = np.linalg.norm(incoming - stored)

    if distance > 15:
        raise HTTPException(401, "Pose mismatch")

    return {"status": "authenticated"}
