import os
from celery import Celery
from core.orchestrator import orchestrator
from db.database import SessionLocal
from models.task import Task

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "multi_agent_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task(bind=True)
def process_task(self, task_id: int):
    """
    Celery task that delegates work to the Orchestrator via LangGraph and tracks status in DB.
    """
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            print(f"Task {task_id} not found in DB.")
            return {"status": "FAILURE", "error": "Task not found"}

        # Update status to processing
        task.status = "processing"
        db.commit()

        print(f"Executing task {task_id} of type: {task.task_type}")
        # Run workflow
        result = orchestrator.route_task(task.task_type, task.payload)
        
        # Update success status
        task.status = "completed"
        task.result = result
        db.commit()
        return {"status": "SUCCESS", "result": result}
    except Exception as e:
        print(f"Error processing task {task_id}: {e}")
        # Attempt to mark failed in DB
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            task.status = "failed"
            task.result = {"error": str(e)}
            db.commit()
        return {"status": "FAILURE", "error": str(e)}
    finally:
        db.close()
