# schemas/journal.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class JournalCreate(BaseModel):
    humor: str
    title: Optional[str] = None
    content: Optional[str] = None
    is_pinned: bool = False
    color: str = "#ffffff"


class JournalUpdate(BaseModel):
    humor: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    is_pinned: Optional[bool] = None
    color: Optional[str] = None
    report: Optional[bool] = None  # Fixed typo: reported -> report


class JournalOut(BaseModel):
    id: int
    user_id: int  # Add this for React Native
    humor: str
    title: Optional[str]
    content: Optional[str]
    is_pinned: bool
    color: str
    report: bool
    created_at: datetime
    updated_at: datetime  # Add this

    class Config:
        from_attributes = True