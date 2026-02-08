from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
from .crud import create_task, get_tasks_by_user, get_task_by_id, update_task, delete_task
from ..database import get_session
from ..models import Task, TaskCreate, TaskUpdate, TaskResponse
from ..auth.middleware import JWTBearer  # ✅ Token check karne ke liye
from typing import List

tasks_router = APIRouter()

@tasks_router.post("/", response_model=TaskResponse)
def create_new_task(
    task: TaskCreate, 
    request: Request, 
    session: Session = Depends(get_session),
    token: str = Depends(JWTBearer()) # ✅ Ye verify karega ke aap login hain
):
    """Create a new task for the authenticated user"""
    # Middleware ne jo ID token se nikaali thi wo yahan milegi
    user_id = getattr(request.state, "user_id", None)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    # Create a new Task instance with user_id and data from TaskCreate
    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=user_id  # Set the authenticated user's ID
    )

    created_task = create_task(session, db_task)
    return created_task

@tasks_router.get("/", response_model=List[TaskResponse])
def read_tasks(
    request: Request,
    skip: int = 0, 
    limit: int = 100, 
    session: Session = Depends(get_session),
    token: str = Depends(JWTBearer())
):
    """Retrieve tasks for the authenticated user"""
    user_id = getattr(request.state, "user_id", None)
    tasks = get_tasks_by_user(session, user_id, skip=skip, limit=limit)
    return tasks

@tasks_router.get("/{task_id}", response_model=TaskResponse)
def read_task(
    task_id: str,
    request: Request,
    session: Session = Depends(get_session),
    token: str = Depends(JWTBearer())
):
    """Retrieve a specific task by ID"""
    user_id = getattr(request.state, "user_id", None)
    task = get_task_by_id(session, task_id, user_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@tasks_router.put("/{task_id}", response_model=TaskResponse)
def update_existing_task(
    task_id: str,
    task_update: TaskUpdate,
    request: Request,
    session: Session = Depends(get_session),
    token: str = Depends(JWTBearer())
):
    """Update a specific task"""
    user_id = getattr(request.state, "user_id", None)
    updated_task = update_task(session, task_id, user_id, task_update.model_dump(exclude_unset=True))

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@tasks_router.delete("/{task_id}")
def delete_existing_task(
    task_id: str,
    request: Request,
    session: Session = Depends(get_session),
    token: str = Depends(JWTBearer())
):
    """Delete a specific task"""
    user_id = getattr(request.state, "user_id", None)
    success = delete_task(session, task_id, user_id)

    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}