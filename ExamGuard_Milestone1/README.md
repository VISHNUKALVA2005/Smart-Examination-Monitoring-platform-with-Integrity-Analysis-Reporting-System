# ExamGuard — Milestone 1 Demo

This demo uses **FastAPI + SQLite**. The project description lists FastAPI in its tech stack, although one Milestone 1 bullet mentions Flask; this package keeps a single FastAPI backend.

## Included
- Candidate registration and login with password hashing and JWT authentication.
- SQLite persistence for users, registration photos, examination sessions, lifecycle events and MCQ answers.
- Registration photo capture and a one-time OpenCV face-presence check (not face recognition or liveness detection).
- Candidate session lifecycle: start, pause, resume and submit.
- A 10-question Computer Science/IT MCQ sample examination, 15-minute browser timer, answer autosave and score on submission.
- Faker-based synthetic session log generator.
- Interactive API documentation at `/docs`.

## Requirements
Windows 10/11 and Python 3.10+ (Python 3.11 recommended). A webcam is optional. VS Code is not required.

## Run using Windows CMD
1. Extract the ZIP.
2. Open CMD and enter the backend folder (replace the path if you extracted elsewhere):

```cmd
cd /d "%USERPROFILE%\Downloads\ExamGuard_Milestone1\backend"
```

3. First-time setup only:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Start the backend:

```cmd
.venv\Scripts\activate.bat
uvicorn main:app --reload
```

Keep this CMD window open. Visit `http://127.0.0.1:8000/health` and `http://127.0.0.1:8000/docs`.

5. Open a second CMD window and start the frontend (adjust the path if needed):

```cmd
cd /d "%USERPROFILE%\Downloads\ExamGuard_Milestone1\frontend"
python -m http.server 5500
```

6. Visit `http://127.0.0.1:5500/register.html`. Register or log in as a candidate.

On later days, do not reinstall packages or recreate `.venv`; just activate it and run Uvicorn. Keep both CMD windows open while using the app.

## Candidate demo flow
Register candidate → log in → Candidate Dashboard → Start Exam → answer MCQs → Pause → Resume → Submit → see score and attempted count. Answers are saved to SQLite as they are selected.

The 15-minute countdown is currently a browser-side demo timer. Server-side timed-exam enforcement is not included. The score is calculated from the answer key on the server when the candidate submits.

## Create staff demo accounts
Run from `backend` with the virtual environment activated:

```cmd
python create_staff.py --name "Demo Invigilator" --email invigilator@example.com --role invigilator
python create_staff.py --name "Demo Admin" --email admin@example.com --role administrator
```

Enter a password of at least 8 characters at the prompt. CMD does not display password characters while typing; that is normal.

## Generate synthetic logs
From `backend` with `.venv` active:

```cmd
python generate_synthetic_logs.py --count 50 --output synthetic_session_logs.csv
```

## Key API endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/auth/register` | Candidate registration |
| POST | `/auth/login` | Candidate/staff login |
| GET | `/auth/me` | Current user |
| POST | `/profile/photo` | Save registration photo |
| GET | `/exams/demo` | Sample MCQ exam |
| POST | `/exams/sessions/{id}/answers` | Save selected answer |
| POST | `/sessions/start` | Start candidate session |
| POST | `/sessions/{id}/pause` | Pause |
| POST | `/sessions/{id}/resume` | Resume |
| POST | `/sessions/{id}/submit` | Submit and calculate demo score |
| GET | `/sessions/mine` | Candidate session history |

## Data locations
- SQLite database: `backend/examguard.db` (created automatically).
- Registration photos: `backend/uploads/registration_photos/`.
- Synthetic CSV: generated in `backend/`.

## Scope note
Continuous face monitoring, browser/tab surveillance, suspicious-event detection, integrity scoring, AI reports and full staff dashboards are later-stage features and are not claimed as implemented here. This is a local academic demo, not a production exam service.


## Frontend account creation (local mentor demo)
The registration page includes Candidate, Invigilator and Administrator roles. This is intentionally enabled for a local classroom demonstration so you can create all three account types without running a backend script. **Do not deploy this open role-selection flow to production**; staff accounts must be provisioned by an authorized administrator in a real system.

## Invigilator workflow
Register an Invigilator account, sign in using the Invigilator role, create an examination, add MCQ questions and correct options, then publish it. Candidates will see published examinations on their dashboard.

## Candidate workflow
Register as Candidate, enable the camera and capture a photo, create the account, sign in, start a published examination, select answers, pause/resume, and submit to see the calculated score.

## Run from Windows CMD
Open two CMD windows. In the backend window:
```cmd
cd /d "PATH\\TO\\ExamGuard_Milestone1\\backend"
.venv\\Scripts\\activate.bat
uvicorn main:app --reload
```
In the frontend window:
```cmd
cd /d "PATH\\TO\\ExamGuard_Milestone1\\frontend"
python -m http.server 5500
```
Open http://127.0.0.1:5500/register.html. Install dependencies only on first setup with `pip install -r requirements.txt`.
Google OAuth is intentionally not implemented; it is reserved for a later configuration step.
