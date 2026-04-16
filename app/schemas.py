# schemas.py — Pydantic request/response validation schemas

from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date as date_type


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    effort: Optional[str] = "medium"
    task_date: Optional[date_type] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    effort: Optional[str] = None
    completed: Optional[bool] = None
    task_date: Optional[date_type] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: str
    effort: str
    completed: bool
    ai_note: Optional[str]
    task_date: Optional[date_type]
    start_time: Optional[str]
    end_time: Optional[str]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True  # allows converting SQLAlchemy model → Pydantic schema


class AIRequest(BaseModel):
    task_ids: list[int]


class PlanContextRequest(BaseModel):
    date: str
    task_ids: list[int]
    next_day_tasks: list[dict] = []