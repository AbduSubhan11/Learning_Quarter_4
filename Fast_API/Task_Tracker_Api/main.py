from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr, EmailStr, validator
from typing import Optional, List
from datetime import date
from uuid import uuid4

app = FastAPI()

users = {}
tasks = {}

# ------------------- Models -------------------

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=20)
    email: EmailStr

class UserRead(BaseModel):
    id: str
    username: str
    email: EmailStr

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "pending"
    due_date: date
    user_id: str

    @validator("due_date")
    def validate_due_date(cls, value):
        if value < date.today():
            raise ValueError("Due date must be today or in the future")
        return value

    @validator("status")
    def validate_status(cls, value):
        if value not in ["pending", "completed"]:
            raise ValueError("Status must be either 'pending' or 'completed'")
        return value

class Task(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: str
    due_date: date
    user_id: str



# ------------------- Routes -------------------

@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate):
    user_id = str(uuid4())
    new_user = {"id": user_id, **user.dict()}
    users[user_id] = new_user
    return new_user

@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: str):
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate):
    if task.user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    task_id = str(uuid4())
    task_data = {"id": task_id, **task.dict()}
    tasks[task_id] = task_data
    return task_data

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task_status(task_id: str, status: str):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if status not in ["pending", "completed"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    task["status"] = status
    return task

@app.get("/users/{user_id}/tasks", response_model=List[Task])
def get_tasks_by_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    user_tasks = [task for task in tasks.values() if task["user_id"] == user_id]
    return user_tasks
