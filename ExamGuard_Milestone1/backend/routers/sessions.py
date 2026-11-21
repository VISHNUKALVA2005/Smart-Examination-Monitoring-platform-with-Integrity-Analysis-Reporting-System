from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import ExamSession, SessionEvent, ExamAnswer, CandidateAnswer, ExaminationQuestion, User
from routers.authentication import get_current_user, require_role

router = APIRouter(prefix="/sessions", tags=["Exam Sessions"])

def now():
    return datetime.now(timezone.utc).replace(tzinfo=None)

def own_session(session_id: int, user: User, db: Session):
    record = db.query(ExamSession).filter(ExamSession.id == session_id, ExamSession.user_id == user.id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Exam session not found")
    return record

def add_event(db, session_id, event_type, description):
    db.add(SessionEvent(session_id=session_id, event_type=event_type, description=description))

@router.post("/start")
def start_session(exam_id: int | None = None, user: User = Depends(require_role("candidate")), db: Session = Depends(get_db)):
    active = db.query(ExamSession).filter(ExamSession.user_id == user.id, ExamSession.status.in_(["in_progress", "paused"])).first()
    if active:
        raise HTTPException(status_code=409, detail="You already have an unfinished exam session")
    rec = ExamSession(user_id=user.id, examination_id=exam_id, status="in_progress", started_at=now())
    db.add(rec); db.flush(); add_event(db, rec.id, "SESSION_STARTED", "Candidate started the examination")
    db.commit(); db.refresh(rec)
    return {"id": rec.id, "status": rec.status, "started_at": rec.started_at}

@router.post("/{session_id}/pause")
def pause_session(session_id: int, user: User = Depends(require_role("candidate")), db: Session = Depends(get_db)):
    rec = own_session(session_id, user, db)
    if rec.status != "in_progress": raise HTTPException(status_code=409, detail="Only an in-progress session can be paused")
    rec.status = "paused"; rec.paused_at = now(); add_event(db, rec.id, "SESSION_PAUSED", "Candidate paused the examination")
    db.commit(); return {"id": rec.id, "status": rec.status}

@router.post("/{session_id}/resume")
def resume_session(session_id: int, user: User = Depends(require_role("candidate")), db: Session = Depends(get_db)):
    rec = own_session(session_id, user, db)
    if rec.status != "paused": raise HTTPException(status_code=409, detail="Only a paused session can be resumed")
    rec.status = "in_progress"; rec.paused_at = None; add_event(db, rec.id, "SESSION_RESUMED", "Candidate resumed the examination")
    db.commit(); return {"id": rec.id, "status": rec.status}

@router.post("/{session_id}/submit")
def submit_session(session_id: int, user: User = Depends(require_role("candidate")), db: Session = Depends(get_db)):
    rec = own_session(session_id, user, db)
    if rec.status not in ("in_progress", "paused"): raise HTTPException(status_code=409, detail="This session cannot be submitted")
    rec.status = "submitted"; rec.submitted_at = now(); add_event(db, rec.id, "SESSION_SUBMITTED", "Candidate submitted the examination")
    answers = db.query(ExamAnswer).filter(ExamAnswer.session_id == rec.id).all()
    score = sum(1 for answer in answers if answer.is_correct)
    answered = len(answers)
    db.commit()
    return {"id": rec.id, "status": rec.status, "submitted_at": rec.submitted_at, "answered": answered, "total_questions": 10, "score": score, "total_marks": 10}

@router.get("/mine")
def my_sessions(user: User = Depends(require_role("candidate")), db: Session = Depends(get_db)):
    records = db.query(ExamSession).filter(ExamSession.user_id == user.id).order_by(ExamSession.id.desc()).all()
    return [{"id": r.id, "status": r.status, "started_at": r.started_at, "paused_at": r.paused_at, "submitted_at": r.submitted_at} for r in records]

@router.get("/{session_id}/events")
def session_events(session_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rec = db.query(ExamSession).filter(ExamSession.id == session_id).first()
    if not rec or (user.role == "candidate" and rec.user_id != user.id): raise HTTPException(status_code=404, detail="Exam session not found")
    events = db.query(SessionEvent).filter(SessionEvent.session_id == session_id).order_by(SessionEvent.id.asc()).all()
    return [{"id": e.id, "event_type": e.event_type, "description": e.description, "occurred_at": e.occurred_at} for e in events]
