"""
MCP Tools for Todo AI Chatbot

These tools provide task management capabilities for the AI agent.
All tools are stateless and enforce user isolation.

Task IDs: T001-T005 (MCP Tools Implementation)
"""

from sqlmodel import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from app.models import Task, TaskCreate, TaskUpdate
from app.tasks.crud import create_task, get_tasks_by_user, get_task_by_id, update_task, delete_task
from app.database import get_session

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# Tool: add_task
# ============================================================================

def add_task_tool(title: str, user_id: str, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new task for the authenticated user.
    
    Args:
        title: Task title (required, 1-255 characters)
        user_id: Authenticated user's ID
        description: Optional task description (max 1000 characters)
    
    Returns:
        Dict with task details or error message
    
    Tool Contract:
        - Input: title (str), user_id (str), description (str, optional)
        - Output: task_id, title, description, completed, created_at
        - Validation: title required, max lengths enforced
        - User Isolation: Task associated with user_id
    """
    try:
        # Validate title
        if not title or not title.strip():
            logger.warning(f"add_task: Empty title for user {user_id}")
            return {"success": False, "error": "Title is required"}
        
        if len(title) > 255:
            logger.warning(f"add_task: Title too long for user {user_id}")
            return {"success": False, "error": "Title must be 255 characters or less"}
        
        # Validate description if provided
        if description and len(description) > 1000:
            logger.warning(f"add_task: Description too long for user {user_id}")
            return {"success": False, "error": "Description must be 1000 characters or less"}
        
        # Create task using existing CRUD
        session = next(get_session())
        try:
            db_task = Task(
                title=title.strip(),
                description=description.strip() if description else None,
                completed=False,
                user_id=user_id
            )
            
            created_task = create_task(session, db_task)
            
            logger.info(f"add_task: Created task {created_task.id} for user {user_id}")
            
            return {
                "success": True,
                "task_id": str(created_task.id),
                "title": created_task.title,
                "description": created_task.description,
                "completed": created_task.completed,
                "created_at": created_task.created_at.isoformat()
            }
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"add_task: Error creating task for user {user_id}: {str(e)}")
        return {"success": False, "error": "Failed to create task"}


# ============================================================================
# Tool: list_tasks
# ============================================================================

def list_tasks_tool(user_id: str, status: str = "all") -> Dict[str, Any]:
    """
    List tasks for the authenticated user with optional status filter.
    
    Args:
        user_id: Authenticated user's ID
        status: Filter by status - "all", "pending", or "completed"
    
    Returns:
        Dict with list of tasks or error message
    
    Tool Contract:
        - Input: user_id (str), status (str: "all"|"pending"|"completed")
        - Output: List of tasks with id, title, completed status
        - User Isolation: Only returns tasks for user_id
    """
    try:
        # Validate status
        valid_statuses = ["all", "pending", "completed"]
        if status not in valid_statuses:
            logger.warning(f"list_tasks: Invalid status '{status}' for user {user_id}")
            return {"success": False, "error": f"Status must be one of: {valid_statuses}"}
        
        # Get tasks using existing CRUD
        session = next(get_session())
        try:
            tasks = get_tasks_by_user(session, user_id, skip=0, limit=100)
            
            # Filter by status if needed
            if status == "pending":
                tasks = [t for t in tasks if not t.completed]
            elif status == "completed":
                tasks = [t for t in tasks if t.completed]
            
            logger.info(f"list_tasks: Retrieved {len(tasks)} tasks for user {user_id} (status: {status})")
            
            return {
                "success": True,
                "count": len(tasks),
                "tasks": [
                    {
                        "task_id": str(task.id),
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat()
                    }
                    for task in tasks
                ]
            }
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"list_tasks: Error retrieving tasks for user {user_id}: {str(e)}")
        return {"success": False, "error": "Failed to retrieve tasks"}


# ============================================================================
# Tool: update_task
# ============================================================================

def update_task_tool(task_id: str, user_id: str, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Update an existing task's title and/or description.
    
    Args:
        task_id: ID of the task to update
        user_id: Authenticated user's ID
        title: New title (optional)
        description: New description (optional)
    
    Returns:
        Dict with updated task details or error message
    
    Tool Contract:
        - Input: task_id (str), user_id (str), title (str, optional), description (str, optional)
        - Output: Updated task details
        - User Isolation: Verifies task belongs to user_id
    """
    try:
        # Validate task_id
        if not task_id:
            logger.warning(f"update_task: Missing task_id for user {user_id}")
            return {"success": False, "error": "Task ID is required"}
        
        # Validate at least one field to update
        if not title and not description:
            logger.warning(f"update_task: No fields to update for user {user_id}")
            return {"success": False, "error": "Provide title or description to update"}
        
        # Validate title length if provided
        if title and len(title) > 255:
            logger.warning(f"update_task: Title too long for user {user_id}")
            return {"success": False, "error": "Title must be 255 characters or less"}
        
        # Validate description length if provided
        if description and len(description) > 1000:
            logger.warning(f"update_task: Description too long for user {user_id}")
            return {"success": False, "error": "Description must be 1000 characters or less"}
        
        # Update task using existing CRUD
        session = next(get_session())
        try:
            # Check if task exists and belongs to user
            existing_task = get_task_by_id(session, task_id, user_id)
            if not existing_task:
                logger.warning(f"update_task: Task {task_id} not found for user {user_id}")
                return {"success": False, "error": "Task not found"}
            
            # Prepare update data
            update_data = {}
            if title:
                update_data["title"] = title.strip()
            if description:
                update_data["description"] = description.strip()
            
            updated_task = update_task(session, task_id, user_id, update_data)
            
            logger.info(f"update_task: Updated task {task_id} for user {user_id}")
            
            return {
                "success": True,
                "task_id": str(updated_task.id),
                "title": updated_task.title,
                "description": updated_task.description,
                "updated_at": updated_task.updated_at.isoformat()
            }
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"update_task: Error updating task {task_id} for user {user_id}: {str(e)}")
        return {"success": False, "error": "Failed to update task"}


# ============================================================================
# Tool: complete_task
# ============================================================================

def complete_task_tool(task_id: str, user_id: str) -> Dict[str, Any]:
    """
    Mark a task as completed.
    
    Args:
        task_id: ID of the task to complete
        user_id: Authenticated user's ID
    
    Returns:
        Dict with updated task details or error message
    
    Tool Contract:
        - Input: task_id (str), user_id (str)
        - Output: Updated task with completed=True
        - User Isolation: Verifies task belongs to user_id
    """
    try:
        # Validate task_id
        if not task_id:
            logger.warning(f"complete_task: Missing task_id for user {user_id}")
            return {"success": False, "error": "Task ID is required"}
        
        # Complete task using existing CRUD
        session = next(get_session())
        try:
            # Check if task exists and belongs to user
            existing_task = get_task_by_id(session, task_id, user_id)
            if not existing_task:
                logger.warning(f"complete_task: Task {task_id} not found for user {user_id}")
                return {"success": False, "error": "Task not found"}
            
            # Check if already completed
            if existing_task.completed:
                logger.info(f"complete_task: Task {task_id} already completed for user {user_id}")
                return {
                    "success": True,
                    "message": "Task is already completed",
                    "task_id": task_id,
                    "already_completed": True
                }
            
            # Mark as completed
            updated_task = update_task(session, task_id, user_id, {"completed": True})
            
            logger.info(f"complete_task: Completed task {task_id} for user {user_id}")
            
            return {
                "success": True,
                "task_id": str(updated_task.id),
                "title": updated_task.title,
                "completed": True,
                "completed_at": updated_task.updated_at.isoformat()
            }
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"complete_task: Error completing task {task_id} for user {user_id}: {str(e)}")
        return {"success": False, "error": "Failed to complete task"}


# ============================================================================
# Tool: delete_task
# ============================================================================

def delete_task_tool(task_id: str, user_id: str) -> Dict[str, Any]:
    """
    Delete an existing task.

    Args:
        task_id: ID of the task to delete
        user_id: Authenticated user's ID

    Returns:
        Dict with success message or error

    Tool Contract:
        - Input: task_id (str), user_id (str)
        - Output: Success message
        - User Isolation: Verifies task belongs to user_id
    """
    try:
        # Validate task_id
        if not task_id:
            logger.warning(f"delete_task: Missing task_id for user {user_id}")
            return {"success": False, "error": "Task ID is required"}

        # Delete task using existing CRUD
        session = next(get_session())
        try:
            # Check if task exists and belongs to user
            existing_task = get_task_by_id(session, task_id, user_id)
            if not existing_task:
                logger.warning(f"delete_task: Task {task_id} not found for user {user_id}")
                return {"success": False, "error": "Task not found"}

            success = delete_task(session, task_id, user_id)

            if success:
                logger.info(f"delete_task: Deleted task {task_id} for user {user_id}")
                return {
                    "success": True,
                    "message": f"Task '{existing_task.title}' deleted successfully",
                    "task_id": task_id
                }
            else:
                logger.error(f"delete_task: Failed to delete task {task_id} for user {user_id}")
                return {"success": False, "error": "Failed to delete task"}
        finally:
            session.close()

    except Exception as e:
        logger.error(f"delete_task: Error deleting task {task_id} for user {user_id}: {str(e)}")
        return {"success": False, "error": "Failed to delete task"}


# ============================================================================
# Tool: get_task
# ============================================================================

def get_task_tool(task_id: str, user_id: str) -> Dict[str, Any]:
    """
    Get details of a specific task.

    Args:
        task_id: ID of the task to retrieve
        user_id: Authenticated user's ID

    Returns:
        Dict with task details or error message

    Tool Contract:
        - Input: task_id (str), user_id (str)
        - Output: Task details (id, title, description, completed, dates)
        - User Isolation: Verifies task belongs to user_id
    """
    try:
        # Validate task_id
        if not task_id:
            logger.warning(f"get_task: Missing task_id for user {user_id}")
            return {"success": False, "error": "Task ID is required"}

        # Get task using existing CRUD
        session = next(get_session())
        try:
            # Check if task exists and belongs to user
            task = get_task_by_id(session, task_id, user_id)
            if not task:
                logger.warning(f"get_task: Task {task_id} not found for user {user_id}")
                return {"success": False, "error": "Task not found"}

            logger.info(f"get_task: Retrieved task {task_id} for user {user_id}")

            return {
                "success": True,
                "task": {
                    "task_id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                }
            }
        finally:
            session.close()

    except Exception as e:
        logger.error(f"get_task: Error retrieving task {task_id} for user {user_id}: {str(e)}")
        return {"success": False, "error": "Failed to retrieve task"}


# ============================================================================
# Tool Registry
# ============================================================================

# Dictionary mapping tool names to functions
# Used by AI agent to discover and invoke tools
MCP_TOOLS = {
    "add_task": add_task_tool,
    "list_tasks": list_tasks_tool,
    "update_task": update_task_tool,
    "complete_task": complete_task_tool,
    "delete_task": delete_task_tool,
    "get_task": get_task_tool,
}


def get_tool_schema(tool_name: str) -> Dict[str, Any]:
    """
    Get the schema definition for a tool.
    Used by AI agent to understand tool parameters.
    """
    schemas = {
        "add_task": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Task title (required)"},
                "user_id": {"type": "string", "description": "Authenticated user ID"},
                "description": {"type": "string", "description": "Optional task description"}
            },
            "required": ["title", "user_id"]
        },
        "list_tasks": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "Authenticated user ID"},
                "status": {"type": "string", "enum": ["all", "pending", "completed"], "description": "Filter by status"}
            },
            "required": ["user_id"]
        },
        "update_task": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "Task ID to update"},
                "user_id": {"type": "string", "description": "Authenticated user ID"},
                "title": {"type": "string", "description": "New title"},
                "description": {"type": "string", "description": "New description"}
            },
            "required": ["task_id", "user_id"]
        },
        "complete_task": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "Task ID to complete"},
                "user_id": {"type": "string", "description": "Authenticated user ID"}
            },
            "required": ["task_id", "user_id"]
        },
        "delete_task": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "Task ID to delete"},
                "user_id": {"type": "string", "description": "Authenticated user ID"}
            },
            "required": ["task_id", "user_id"]
        },
        "get_task": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "Task ID to retrieve"},
                "user_id": {"type": "string", "description": "Authenticated user ID"}
            },
            "required": ["task_id", "user_id"]
        }
    }
    return schemas.get(tool_name, {})
