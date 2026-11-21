import os, hashlib, hmac, secrets
from datetime import datetime, timedelta, timezone
import jwt

SECRET_KEY = os.getenv("EXAMGUARD_SECRET_KEY", "CHANGE-ME-TO-A-LONG-RANDOM-SECRET-BEFORE-DEPLOYMENT")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

# Dependency-free password hashing using scrypt (salted, deliberately expensive).
def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=32)
    return f"scrypt${salt.hex()}${digest.hex()}"

def verify_password(password: str, hashed_password: str) -> bool:
    try:
        algorithm, salt_hex, digest_hex = hashed_password.split("$", 2)
        if algorithm != "scrypt": return False
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
        actual = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=len(expected))
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False

def create_access_token(user_id: int, role: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "role": role, "exp": expires}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
