from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import get_db
from models import ExamSession, ExamAnswer, User
from routers.authentication import require_role

router = APIRouter(prefix="/exams", tags=["Sample Examination"])
QUESTIONS = [
 {"number":1,"question":"Which language is commonly used for backend development?","options":{"A":"HTML","B":"Python","C":"CSS","D":"XML"},"correct":"B"},
 {"number":2,"question":"What does CPU stand for?","options":{"A":"Central Processing Unit","B":"Computer Personal Unit","C":"Central Program Utility","D":"Control Processing User"},"correct":"A"},
 {"number":3,"question":"Which data structure follows FIFO?","options":{"A":"Stack","B":"Tree","C":"Queue","D":"Graph"},"correct":"C"},
 {"number":4,"question":"Which SQL command retrieves data from a table?","options":{"A":"INSERT","B":"UPDATE","C":"DELETE","D":"SELECT"},"correct":"D"},
 {"number":5,"question":"What does HTTP stand for?","options":{"A":"HyperText Transfer Protocol","B":"High Transfer Text Program","C":"Hyperlink Transfer Process","D":"Host Text Transfer Protocol"},"correct":"A"},
 {"number":6,"question":"Which one is an operating system?","options":{"A":"MySQL","B":"Linux","C":"Python","D":"HTML"},"correct":"B"},
 {"number":7,"question":"What is the time complexity of binary search on a sorted array?","options":{"A":"O(n)","B":"O(n²)","C":"O(log n)","D":"O(1) always"},"correct":"C"},
 {"number":8,"question":"Which protocol is used for secure web browsing?","options":{"A":"FTP","B":"HTTP","C":"SMTP","D":"HTTPS"},"correct":"D"},
 {"number":9,"question":"Which of these is a relational database?","options":{"A":"SQLite","B":"JPEG","C":"CSS","D":"MP3"},"correct":"A"},
 {"number":10,"question":"What does API stand for?","options":{"A":"Application Programming Interface","B":"Applied Program Internet","C":"Automated Programming Input","D":"Application Process Integration"},"correct":"A"},
]
class AnswerInput(BaseModel):
 question_number: int = Field(ge=1, le=10)
 selected_option: str = Field(pattern="^[ABCD]$")

@router.get("/demo")
def get_demo_exam(user: User = Depends(require_role("candidate"))):
 return {"id":"examguard-demo-01","title":"ExamGuard — Demo Examination","description":"Basic Computer Science and IT Fundamentals","duration_minutes":15,"total_questions":len(QUESTIONS),"total_marks":len(QUESTIONS),"questions":[{"number":q["number"],"question":q["question"],"options":q["options"]} for q in QUESTIONS]}

@router.post("/sessions/{session_id}/answers")
def save_answer(session_id:int, payload:AnswerInput, user:User=Depends(require_role("candidate")), db:Session=Depends(get_db)):
 session=db.query(ExamSession).filter(ExamSession.id==session_id,ExamSession.user_id==user.id).first()
 if not session: raise HTTPException(status_code=404,detail="Exam session not found")
 if session.status!="in_progress": raise HTTPException(status_code=409,detail="Answers can only be changed while the exam is in progress")
 question=QUESTIONS[payload.question_number-1]
 answer=db.query(ExamAnswer).filter(ExamAnswer.session_id==session_id,ExamAnswer.question_number==payload.question_number).first()
 if answer is None:
  answer=ExamAnswer(session_id=session_id,question_number=payload.question_number,selected_option=payload.selected_option,is_correct=payload.selected_option==question["correct"]); db.add(answer)
 else:
  answer.selected_option=payload.selected_option; answer.is_correct=payload.selected_option==question["correct"]
 db.commit(); return {"saved":True,"question_number":payload.question_number}
