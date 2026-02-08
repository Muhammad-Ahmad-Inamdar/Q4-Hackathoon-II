"""
Todo domain model for the CLI Todo Application.

This module defines the core data structure and business logic
for todo items in the application.
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Todo:
    """Represents a single todo item"""
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = None
    updated_at: datetime = None
    deadline: Optional[datetime] = None

    def __post_init__(self):
        """Initialize datetime fields if not provided"""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

        # Validate required fields
        if not self.title or not self.title.strip():
            raise ValueError("Title is required and cannot be empty")

    def complete(self) -> None:
        """Mark the todo as complete"""
        self.completed = True
        self.updated_at = datetime.now()

    def incomplete(self) -> None:
        """Mark the todo as incomplete"""
        self.completed = False
        self.updated_at = datetime.now()

    def update(self, title: Optional[str] = None, description: Optional[str] = None, deadline: Optional[datetime] = None) -> None:
        """Update todo details"""
        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty")
            self.title = title.strip()

        if description is not None:
            self.description = description

        if deadline is not None:
            self.deadline = deadline

        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """Convert todo to dictionary representation"""
        result = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

        # Include deadline if it exists
        if self.deadline:
            result['deadline'] = self.deadline.isoformat()
        else:
            result['deadline'] = None

        return result