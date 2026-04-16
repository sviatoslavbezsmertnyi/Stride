# models.py — SQLAlchemy database models

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Date
from sqlalchemy.sql import func
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(20), default="medium")   # low / medium / high / urgent
    effort = Column(String(20), default="medium")     # low / medium / high
    completed = Column(Boolean, default=False)
    ai_note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    task_date = Column(Date, nullable=True)
    start_time = Column(String(5), nullable=True)     # e.g. "09:00"
    end_time = Column(String(5), nullable=True)       # e.g. "10:30"
