from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime

class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: str = Field(default="candidate", pattern="^(candidate|invigilator|administrator)$")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)
    role: str = Field(pattern="^(candidate|invigilator|administrator)$")

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    email: EmailStr
    role: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class SessionResponse(BaseModel):
    id: int
    status: str
    started_at: datetime | None = None
    paused_at: datetime | None = None
    submitted_at: datetime | None = None
