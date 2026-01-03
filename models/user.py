from sqlalchemy import Column, Integer, String, Boolean, DateTime, Time
from datetime import datetime
from core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    role = Column(String, default="patient")
    emotions_kw = Column(String, nullable=False, default="[]")

    # Volunteer availability fields
    availability_date = Column(DateTime, nullable=True)  # Next available date
    availability_start_time = Column(Time, nullable=True)  # Start time (HH:MM)
    availability_end_time = Column(Time, nullable=True)  # End time (HH:MM)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

