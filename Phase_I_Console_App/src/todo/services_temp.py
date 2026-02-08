"""
Service layer for Todo operations.

This module orchestrates business operations for Todo items,
mediating between the CLI layer and the repository layer.
"""
from typing import List, Optional
from datetime import datetime
from .models import Todo
from .repository import TodoRepository


class TodoService:
    """Service class for managing todo operations"""

    def __init__(self, repository: TodoRepository):
        """Initialize the service with a repository"""
        self.repository = repository

    def add_task(self, title: str, description: Optional[str] = None, deadline: Optional[datetime] = None) -> Todo:
        """Create and add a new task with optional deadline"""
        # Create a new Todo instance with a default ID (will be auto-assigned)
        todo = Todo(id=0, title=title, description=description, completed=False, deadline=deadline)
        return self.repository.add(todo)

    def get_all_tasks(self) -> List[Todo]:
        """Retrieve all tasks"""
        return self.repository.get_all()

    def get_task_by_id(self, id: int) -> Optional[Todo]:
        """Retrieve a specific task by ID"""
        return self.repository.get_by_id(id)

    def update_task(self, id: int, title: Optional[str] = None, description: Optional[str] = None, deadline: Optional[datetime] = None) -> Optional[Todo]:
        """Update task details while preserving completion status"""
        existing_todo = self.repository.get_by_id(id)
        if existing_todo is None:
            return None

        # Preserve the completion status
        completed_status = existing_todo.completed

        # Update the todo details
        existing_todo.update(title=title, description=description, deadline=deadline)

        # Restore the completion status
        existing_todo.completed = completed_status

        # Save the updated todo
        return self.repository.update(existing_todo)

    def complete_task(self, id: int) -> Optional[Todo]:
        """Mark a task as complete"""
        todo = self.repository.get_by_id(id)
        if todo is None:
            return None

        todo.complete()
        return self.repository.update(todo)

    def incomplete_task(self, id: int) -> Optional[Todo]:
        """Mark a task as incomplete"""
        todo = self.repository.get_by_id(id)
        if todo is None:
            return None

        todo.incomplete()
        return self.repository.update(todo)

    def delete_task(self, id: int) -> bool:
        """Delete a task by ID"""
        return self.repository.delete(id)

    def get_tasks_by_status(self, status: bool) -> List[Todo]:
        """Get tasks filtered by completion status"""
        return self.repository.get_by_status(status)

    def sort_tasks(self, tasks: List[Todo], sort_by: str = "created_at", order: str = "asc") -> List[Todo]:
        """Sort tasks by specified field"""
        reverse = order.lower() == "desc"

        if sort_by.lower() == "created_at":
            return sorted(tasks, key=lambda x: x.created_at or datetime.min, reverse=reverse)
        elif sort_by.lower() == "deadline":
            # Sort by deadline, with tasks without deadlines at the end
            def deadline_sort_key(todo):
                if todo.deadline is None:
                    # Put tasks without deadlines at the end (or beginning based on order)
                    return datetime.max if not reverse else datetime.min
                return todo.deadline
            return sorted(tasks, key=deadline_sort_key, reverse=reverse)
        elif sort_by.lower() == "status":
            # Sort by completion status (completed last by default)
            return sorted(tasks, key=lambda x: x.completed, reverse=reverse)
        else:
            # Default to sorting by creation date
            return sorted(tasks, key=lambda x: x.created_at or datetime.min, reverse=reverse)

    def filter_tasks_by_status(self, tasks: List[Todo], status: bool) -> List[Todo]:
        """Filter tasks by completion status"""
        return [task for task in tasks if task.completed == status]

    def get_sorted_tasks(self, sort_by: str = "created_at", order: str = "asc") -> List[Todo]:
        """Get all tasks sorted by specified field"""
        all_tasks = self.get_all_tasks()
        return self.sort_tasks(all_tasks, sort_by, order)

    def get_filtered_tasks(self, status: bool) -> List[Todo]:
        """Get tasks filtered by completion status"""
        return self.get_tasks_by_status(status)