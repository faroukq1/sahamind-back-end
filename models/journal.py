from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from core.database import Base

class Journal(Base):
    __tablename__ = "journals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    humor = Column(String, nullable=False)   # e.g. sad, anxious, calm
    title = Column(String, nullable=True)
    content = Column(Text, nullable=False)

    report= Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
