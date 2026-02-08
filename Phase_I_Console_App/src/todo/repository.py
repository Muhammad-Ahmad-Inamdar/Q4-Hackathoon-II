"""
File-based repository for Todo items.

This module manages the storage and retrieval of Todo items
with file persistence between application sessions.
"""
import json
import os
from typing import Dict, List, Optional
from .models import Todo


class TodoRepository:
    """File-based repository for managing Todo items with persistence"""

    def __init__(self, file_path: str = "todos.json"):
        """Initialize the repository with file persistence"""
        self._storage: Dict[int, Todo] = {}
        self._next_id = 1
        self._file_path = file_path

        # Load existing data from file if it exists
        self._load_from_file()

    def _load_from_file(self):
        """Load todos from the persistence file"""
        if os.path.exists(self._file_path):
            try:
                with open(self._file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                for item in data:
                    # Create Todo object from the data
                    todo = Todo(
                        id=item['id'],
                        title=item['title'],
                        description=item.get('description'),
                        completed=item.get('completed', False)
                    )
                    # Set datetime values if they exist
                    from datetime import datetime
                    if 'created_at' in item:
                        todo.created_at = datetime.fromisoformat(item['created_at'])
                    if 'updated_at' in item:
                        todo.updated_at = datetime.fromisoformat(item['updated_at'])
                    if 'deadline' in item and item['deadline'] is not None:
                        todo.deadline = datetime.fromisoformat(item['deadline'])

                    # Add to storage and update next_id if needed
                    self._storage[todo.id] = todo
                    if todo.id >= self._next_id:
                        self._next_id = todo.id + 1
            except (json.JSONDecodeError, KeyError, ValueError):
                # If there's an error loading the file, start with empty storage
                self._storage = {}
                self._next_id = 1

    def _save_to_file(self):
        """Save todos to the persistence file"""
        data = []
        for todo in self._storage.values():
            data.append(todo.to_dict())

        try:
            with open(self._file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except IOError:
            # Handle file write errors gracefully
            pass

    def add(self, todo: Todo) -> Todo:
        """Add a new todo to the repository"""
        # Assign an ID if the todo doesn't have one
        if todo.id is None or todo.id == 0:
            todo.id = self._next_id
            self._next_id += 1

        # If the ID is greater than or equal to our next ID, update the next ID
        if todo.id >= self._next_id:
            self._next_id = todo.id + 1

        self._storage[todo.id] = todo
        # Save to file after modification
        self._save_to_file()
        return todo

    def get_by_id(self, id: int) -> Optional[Todo]:
        """Retrieve a todo by its ID"""
        return self._storage.get(id)

    def get_all(self) -> List[Todo]:
        """Retrieve all todos"""
        return list(self._storage.values())

    def update(self, todo: Todo) -> Optional[Todo]:
        """Update an existing todo"""
        if todo.id in self._storage:
            self._storage[todo.id] = todo
            # Save to file after modification
            self._save_to_file()
            return todo
        return None

    def delete(self, id: int) -> bool:
        """Delete a todo by its ID"""
        if id in self._storage:
            del self._storage[id]
            # Save to file after modification
            self._save_to_file()
            return True
        return False

    def get_by_status(self, status: bool) -> List[Todo]:
        """Filter todos by completion status"""
        return [todo for todo in self._storage.values() if todo.completed == status]