from sqlmodel import Session, select
from ..models import Task
from typing import List, Optional
from sqlalchemy import func


def create_task(session: Session, task: Task) -> Task:
    """Create a new task"""
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_tasks_by_user(session: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[Task]:
    """Get tasks for a specific user with pagination"""
    statement = select(Task).where(Task.user_id == user_id).offset(skip).limit(limit)
    tasks = session.exec(statement).all()
    return tasks


def get_task_by_id(session: Session, task_id: str, user_id: str) -> Optional[Task]:
    """Get a specific task by ID for a specific user"""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    return task


def update_task(session: Session, task_id: str, user_id: str, task_update: dict) -> Optional[Task]:
    """Update a specific task"""
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return None

    for field, value in task_update.items():
        setattr(task, field, value)

    task.updated_at = func.now()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task_id: str, user_id: str) -> bool:
    """Delete a specific task"""
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return False

    session.delete(task)
    session.commit()
    return True


