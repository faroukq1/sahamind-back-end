from pydantic import BaseModel, EmailStr
from typing import List

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    emotions_kw: List[str] = []


class UserLogin(BaseModel):
    email: EmailStr
    password: str
