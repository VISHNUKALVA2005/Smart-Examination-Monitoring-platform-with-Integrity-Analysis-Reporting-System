from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import get_db
from models import Examination, ExaminationQuestion, ExamSession, CandidateAnswer, User
from routers.authentication import require_role

router=APIRouter(prefix="/examinations",tags=["Examinations"])

class QuestionIn(BaseModel):
    question_text:str=Field(min_length=5)
    option_a:str; option_b:str; option_c:str; option_d:str
    correct_option:str=Field(pattern="^[ABCD]$")
class ExamIn(BaseModel):
    title:str=Field(min_length=3,max_length=200)
    description:str=""
    duration_minutes:int=Field(ge=1,le=180)
    questions:list[QuestionIn]=Field(min_length=1,max_length=50)

def pack(e, include_answers=False):
    qs=[]
    for q in e.questions:
        item={"id":q.id,"question_text":q.question_text,"options":{"A":q.option_a,"B":q.option_b,"C":q.option_c,"D":q.option_d}}
        if include_answers:item["correct_option"]=q.correct_option
        qs.append(item)
    return {"id":e.id,"title":e.title,"description":e.description,"duration_minutes":e.duration_minutes,"questions":qs,"total_marks":len(qs)}

@router.post("")
def create_exam(data:ExamIn,user:User=Depends(require_role("invigilator","administrator")),db:Session=Depends(get_db)):
    e=Examination(title=data.title,description=data.description,duration_minutes=data.duration_minutes,created_by=user.id,is_published=True)
    db.add(e);db.flush()
    for q in data.questions:
        db.add(ExaminationQuestion(examination_id=e.id,**q.model_dump()))
    db.commit();db.refresh(e)
    return pack(e)

@router.get("")
def list_exams(user:User=Depends(require_role("candidate","invigilator","administrator")),db:Session=Depends(get_db)):
    exams=db.query(Examination).filter(Examination.is_published==True).order_by(Examination.id.desc()).all()
    return [pack(e) for e in exams]

@router.get("/{exam_id}")
def get_exam(exam_id:int,user:User=Depends(require_role("candidate","invigilator","administrator")),db:Session=Depends(get_db)):
    e=db.query(Examination).filter(Examination.id==exam_id,Examination.is_published==True).first()
    if not e:raise HTTPException(404,"Examination not found")
    return pack(e)

@router.post("/{exam_id}/sessions/{session_id}/answers")
def answer(exam_id:int,session_id:int,payload:dict,user:User=Depends(require_role("candidate")),db:Session=Depends(get_db)):
    s=db.query(ExamSession).filter_by(id=session_id,user_id=user.id,examination_id=exam_id).first()
    if not s or s.status!="in_progress":raise HTTPException(409,"No active examination session")
    qid=int(payload.get("question_id",0)); opt=str(payload.get("selected_option",""))
    q=db.query(ExaminationQuestion).filter_by(id=qid,examination_id=exam_id).first()
    if not q or opt not in "ABCD" or len(opt)!=1:raise HTTPException(400,"Invalid answer")
    a=db.query(CandidateAnswer).filter_by(session_id=s.id,question_id=qid).first()
    if a:a.selected_option=opt
    else:db.add(CandidateAnswer(session_id=s.id,question_id=qid,selected_option=opt))
    db.commit();return {"saved":True}
