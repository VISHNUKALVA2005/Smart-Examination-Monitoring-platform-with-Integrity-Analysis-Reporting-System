"""Create an invigilator or administrator account from the backend folder.

Example:
python create_staff.py --name "Exam Admin" --email admin@example.com --role administrator
You will be prompted for the password. Do not commit real credentials.
"""
import argparse
import getpass
from database import Base, engine, SessionLocal
from models import User
from auth_utils import hash_password

Base.metadata.create_all(bind=engine)
parser = argparse.ArgumentParser()
parser.add_argument("--name", required=True)
parser.add_argument("--email", required=True)
parser.add_argument("--role", required=True, choices=["invigilator", "administrator"])
args = parser.parse_args()
password = getpass.getpass("Password (minimum 8 characters): ")
if len(password) < 8:
    raise SystemExit("Password must contain at least 8 characters.")
db = SessionLocal()
try:
    email = args.email.lower()
    if db.query(User).filter(User.email == email).first():
        raise SystemExit("An account with this email already exists.")
    user = User(full_name=args.name, email=email, hashed_password=hash_password(password), role=args.role)
    db.add(user)
    db.commit()
    print(f"Created {args.role} account for {email}")
finally:
    db.close()
