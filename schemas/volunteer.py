# schemas/volunteer.py

from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime, time
import json


class VolunteerResponse(BaseModel):
    id: int
    email: str
    role: str
    emotions_kw: List[str]
    
    # Availability information
    availability_date: Optional[datetime] = None
    availability_start_time: Optional[time] = None
    availability_end_time: Optional[time] = None
    
    is_active: bool
    created_at: datetime

    @field_validator('emotions_kw', mode='before')
    @classmethod
    def parse_emotions_kw(cls, v):
        """Parse emotions_kw from JSON string to list"""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return []
        return v or []

    class Config:
        from_attributes = True
