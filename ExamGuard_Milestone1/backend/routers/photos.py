import base64, re
from pathlib import Path
import cv2
import numpy as np
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import get_db
from models import RegistrationPhoto, User
from routers.authentication import require_role

router = APIRouter(prefix="/profile", tags=["Registration Photo"])
PHOTO_DIR = Path(__file__).resolve().parents[1] / "uploads" / "registration_photos"
PHOTO_DIR.mkdir(parents=True, exist_ok=True)

class PhotoPayload(BaseModel):
    image_data: str = Field(min_length=50, max_length=5_000_000)

@router.post("/photo")
def save_registration_photo(payload: PhotoPayload, user: User = Depends(require_role("candidate")), db: Session = Depends(get_db)):
    match = re.fullmatch(r"data:image/(jpeg|jpg|png);base64,([A-Za-z0-9+/=]+)", payload.image_data)
    if not match: raise HTTPException(status_code=400, detail="Send a JPEG or PNG camera image")
    try:
        raw = base64.b64decode(match.group(2), validate=True)
        arr = np.frombuffer(raw, dtype=np.uint8)
        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if frame is None: raise ValueError("Invalid image")
    except Exception:
        raise HTTPException(status_code=400, detail="The captured image could not be decoded")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(cascade_path)
    faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
    file_path = PHOTO_DIR / f"candidate_{user.id}.jpg"
    if not cv2.imwrite(str(file_path), frame): raise HTTPException(status_code=500, detail="Could not save photo")
    record = db.query(RegistrationPhoto).filter(RegistrationPhoto.user_id == user.id).first()
    if record is None: record = RegistrationPhoto(user_id=user.id, file_path=str(file_path))
    record.file_path = str(file_path); record.face_detected = len(faces) > 0
    db.add(record); db.commit()
    return {"message": "Registration photo saved", "face_detected": bool(len(faces)), "faces_detected": int(len(faces))}
