# main.py — FastAPI application entry point and route definitions

from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.database import get_db, engine
from app import models, schemas
from app.ai import analyze_and_prioritize, generate_daily_plan

# Create all DB tables on startup (like running a migration)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Stride",
    description="AI-powered daily planner",
    version="0.1.0"
)

# Serve static files (HTML frontend) from the /static folder
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", include_in_schema=False)
def root():
    """Serve the frontend."""
    return FileResponse("static/index.html")


# ─── TASK ROUTES ────────────────────────────────────────────────────────────

@app.get("/tasks", response_model=List[schemas.TaskResponse])
def get_tasks(date: Optional[str] = None, db: Session = Depends(get_db)):
    """Get tasks, optionally filtered by date (YYYY-MM-DD)."""
    from datetime import date as date_type
    query = db.query(models.Task)
    if date:
        query = query.filter(models.Task.task_date == date_type.fromisoformat(date))
    return query.order_by(models.Task.created_at.desc()).all()


@app.post("/tasks", response_model=schemas.TaskResponse, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Create a new task."""
    db_task = models.Task(**task.model_dump())  # unpack dict into model fields
    db.add(db_task)
    db.commit()
    db.refresh(db_task)  # reload from DB to get generated id, timestamps
    return db_task
    

@app.patch("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, updates: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """Update any fields of a task (PATCH = partial update)."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Only update fields that were actually sent (not None)
    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()


# ─── AI ROUTES ──────────────────────────────────────────────────────────────

@app.post("/ai/analyze")
def ai_analyze(request: schemas.AIRequest, db: Session = Depends(get_db)):
    """Ask Claude to analyze selected tasks and add insights."""
    tasks = db.query(models.Task).filter(models.Task.id.in_(request.task_ids)).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")

    task_dicts = [
        {"id": t.id, "title": t.title, "description": t.description,
         "priority": t.priority, "effort": t.effort}
        for t in tasks
    ]

    analyzed = analyze_and_prioritize(task_dicts)

    # Save AI notes back to DB
    notes_map = {t["id"]: t["ai_note"] for t in analyzed}
    for task in tasks:
        task.ai_note = notes_map.get(task.id)
    db.commit()

    return {"message": "Analysis complete", "tasks_analyzed": len(tasks)}


@app.post("/ai/plan-with-context")
def ai_plan_with_context(request: schemas.PlanContextRequest, db: Session = Depends(get_db)):
    """Generate a plan with awareness of next day's schedule."""
    tasks = db.query(models.Task).filter(models.Task.id.in_(request.task_ids)).all()
    task_dicts = [
        {"title": t.title, "priority": t.priority,
         "effort": t.effort, "completed": t.completed,
         "start_time": t.start_time}
        for t in tasks
    ]

    # Check for early next-day commitments
    context_note = None
    early_tasks = [t for t in request.next_day_tasks if t.get("start_time") and t["start_time"] < "08:00"]
    if early_tasks:
        earliest = min(early_tasks, key=lambda t: t["start_time"])
        context_note = f"You have '{earliest['title']}' at {earliest['start_time']} tomorrow — consider wrapping up early and getting to bed by 22:00."

    plan = generate_daily_plan(task_dicts)
    return {"plan": plan, "context_note": context_note}
