from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers.authentication import router as auth_router
from routers.sessions import router as sessions_router
from routers.photos import router as photos_router
from routers.exams import router as exams_router
from routers.examinations import router as examinations_router
import models  # noqa: F401 - registers all SQLAlchemy models before create_all

Base.metadata.create_all(bind=engine)
app = FastAPI(title="ExamGuard - Milestone 1 API", version="1.1.0", description="Candidate authentication, registration photo capture and exam session lifecycle")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth_router)
app.include_router(sessions_router)
app.include_router(photos_router)
app.include_router(exams_router)
app.include_router(examinations_router)

@app.get("/")
def root(): return {"message": "ExamGuard Milestone 1 API is running", "docs": "/docs"}

@app.get("/health")
def health(): return {"status": "ok"}
