from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from workers.celery_worker import process_task
from db.database import get_db
from models.task import Task

router = APIRouter()

class TaskRequest(BaseModel):
    task_type: str = "langgraph_flow"
    payload: dict

@router.post("/tasks/")
def create_task(request: TaskRequest, db: Session = Depends(get_db)):
    """
    Submit a new task to the multi-agent system.
    """
    # Create task record in database
    db_task = Task(task_type=request.task_type, payload=request.payload, status="pending")
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Trigger Celery worker asynchronously
    process_task.delay(db_task.id)
    return {"task_id": db_task.id, "status": "Task submitted successfully"}

@router.get("/tasks/")
def list_tasks(db: Session = Depends(get_db)):
    """
    Get the recent list of tasks.
    """
    tasks = db.query(Task).order_by(Task.created_at.desc()).limit(20).all()
    return tasks

@router.get("/tasks/{task_id}")
def get_task_status(task_id: int, db: Session = Depends(get_db)):
    """
    Check the specific status and result of a task.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
