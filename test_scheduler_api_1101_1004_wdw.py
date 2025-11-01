# 代码生成时间: 2025-11-01 10:04:44
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List
import datetime

app = FastAPI(title="Test Scheduler API")
router = APIRouter()

# Pydantic model for task details
class Task(BaseModel):
    id: int
    name: str
    start_time: datetime.datetime
    end_time: datetime.datetime

# Mock database for tasks
tasks_db = [
    {
        "id": 1,
        "name": "Test Task 1",
        "start_time": datetime.datetime(2023, 12, 25, 8, 0),
        "end_time": datetime.datetime(2023, 12, 25, 10, 0)
    },
    {
        "id": 2,
        "name": "Test Task 2",
        "start_time": datetime.datetime(2023, 12, 25, 11, 0),
        "end_time": datetime.datetime(2023, 12, 25, 13, 0)
    }
]

# Get tasks endpoint
@router.get("/tasks/", response_model=List[Task])
async def get_tasks():
    return tasks_db

# Get task by ID endpoint
@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    if task_id < 1 or task_id > len(tasks_db):
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[task_id - 1]

# Add task endpoint
@router.post("/tasks/")
async def add_task(task: Task):
    if any(t['id'] == task.id for t in tasks_db):
        raise HTTPException(status_code=400, detail="Task with this ID already exists")
    task.id = len(tasks_db) + 1  # Assign new ID
    tasks_db.append(task.dict())
    return task

# Error handling
@app.exception_handler(404)
async def not_found_exception_handler(request, exc):
    return {
        "detail": exc.detail,
        "message": "The requested resource was not found."
    }, 404

# Include router in app
app.include_router(router)

# Print Swagger UI URL
print("Open your browser and go to: http://127.0.0.1:8000/docs")
