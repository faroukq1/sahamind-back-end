from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JournalCreate(BaseModel):
    humor: str
    title: Optional[str] = None
    content: Optional[str] = None


class JournalUpdate(BaseModel):
    humor: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    reported: Optional[bool] = None


class JournalOut(BaseModel):
    id: int
    humor: str
    title: Optional[str]
    content: Optional[str]
    report: bool
    created_at: datetime

    class Config:
        from_attributes = True
