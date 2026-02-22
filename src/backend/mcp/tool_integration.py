"""
MCP Tool Integration for OpenAI Agents SDK

This module provides integration between MCP tools and the OpenAI Agents SDK.
It converts MCP tool definitions to the format expected by the Agents SDK.

Task IDs: T001-T005, T026-T030 (MCP Tools + AI Agent Orchestration)
"""

import logging
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime

logger = logging.getLogger(__name__)


class MCPToolWrapper:
    """
    Wrapper for MCP tools to integrate with OpenAI Agents SDK.

    The OpenAI Agents SDK expects tools in a specific format. This wrapper
    converts our MCP tool functions to that format.
    """

    def __init__(self, name: str, func: Callable, description: str, parameters: Dict[str, Any]):
        """
        Initialize tool wrapper.

        Args:
            name: Tool name
            func: Tool function
            description: Tool description
            parameters: JSON Schema for tool parameters
        """
        self.name = name
        self.func = func
        self.description = description
        self.parameters = parameters

    def to_agent_tool(self) -> Dict[str, Any]:
        """
        Convert to OpenAI Agents SDK tool format.

        Returns:
            Dict in OpenAI function calling format
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    async def execute(self, **kwargs) -> Any:
        """
        Execute the tool with given arguments.

        Args:
            **kwargs: Tool arguments

        Returns:
            Tool execution result
        """
        logger.info(f"MCPToolWrapper: Executing '{self.name}' with args: {kwargs}")
        try:
            result = self.func(**kwargs)
            logger.info(f"MCPToolWrapper: '{self.name}' executed successfully")
            return result
        except Exception as e:
            logger.error(f"MCPToolWrapper: '{self.name}' execution error: {str(e)}")
            return {"success": False, "error": str(e)}


def create_mcp_tool_wrappers(mcp_tools: Dict[str, Callable]) -> List[MCPToolWrapper]:
    """
    Create tool wrappers for all MCP tools.

    Args:
        mcp_tools: Dictionary of MCP tool functions

    Returns:
        List of MCPToolWrapper instances
    """
    wrappers = []

    # Tool descriptions and schemas
    tool_configs = {
        "add_task": {
            "description": "Create a new task for the user. Requires title and user_id. Description is optional.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Task title (1-255 characters)",
                    },
                    "user_id": {
                        "type": "string",
                        "description": "Authenticated user's ID",
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description (max 1000 characters)",
                    },
                },
                "required": ["title", "user_id"],
            },
        },
        "list_tasks": {
            "description": "List tasks for the user. Can filter by status (all, pending, completed).",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "Authenticated user's ID",
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by status",
                        "enum": ["all", "pending", "completed"],
                    },
                },
                "required": ["user_id"],
            },
        },
        "update_task": {
            "description": "Update a task's title and/or description. Requires task_id and user_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "Task ID to update",
                    },
                    "user_id": {
                        "type": "string",
                        "description": "Authenticated user's ID",
                    },
                    "title": {
                        "type": "string",
                        "description": "New title (optional)",
                    },
                    "description": {
                        "type": "string",
                        "description": "New description (optional)",
                    },
                },
                "required": ["task_id", "user_id"],
            },
        },
        "complete_task": {
            "description": "Mark a task as completed. Requires task_id and user_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "Task ID to complete",
                    },
                    "user_id": {
                        "type": "string",
                        "description": "Authenticated user's ID",
                    },
                },
                "required": ["task_id", "user_id"],
            },
        },
        "delete_task": {
            "description": "Delete a task permanently. Requires task_id and user_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "Task ID to delete",
                    },
                    "user_id": {
                        "type": "string",
                        "description": "Authenticated user's ID",
                    },
                },
                "required": ["task_id", "user_id"],
            },
        },
        "get_task": {
            "description": "Get details of a specific task by ID. Requires task_id and user_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "Task ID to retrieve",
                    },
                    "user_id": {
                        "type": "string",
                        "description": "Authenticated user's ID",
                    },
                },
                "required": ["task_id", "user_id"],
            },
        },
    }

    for tool_name, tool_func in mcp_tools.items():
        config = tool_configs.get(tool_name, {})
        wrapper = MCPToolWrapper(
            name=tool_name,
            func=tool_func,
            description=config.get("description", f"Execute {tool_name} operation"),
            parameters=config.get("parameters", {}),
        )
        wrappers.append(wrapper)

    return wrappers


def get_tools_for_agent(mcp_tools: Dict[str, Callable]) -> List[Dict[str, Any]]:
    """
    Get tools formatted for OpenAI Agents SDK.

    Args:
        mcp_tools: Dictionary of MCP tool functions

    Returns:
        List of tool definitions in OpenAI format
    """
    wrappers = create_mcp_tool_wrappers(mcp_tools)
    return [wrapper.to_agent_tool() for wrapper in wrappers]


# ============================================================================
# Tool Execution Helper
# ============================================================================

class ToolExecutor:
    """
    Helper class for executing MCP tools with proper error handling.
    """

    def __init__(self, user_id: str, mcp_tools: Dict[str, Callable]):
        """
        Initialize tool executor.

        Args:
            user_id: Authenticated user's ID
            mcp_tools: Dictionary of MCP tool functions
        """
        self.user_id = user_id
        self.mcp_tools = mcp_tools
        self.wrappers = {w.name: w for w in create_mcp_tool_wrappers(mcp_tools)}

    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool with given arguments.

        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments

        Returns:
            Tool execution result
        """
        wrapper = self.wrappers.get(tool_name)

        if not wrapper:
            logger.error(f"ToolExecutor: Tool '{tool_name}' not found")
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}",
            }

        # Add user_id if not provided
        if "user_id" not in arguments:
            arguments["user_id"] = self.user_id

        return wrapper.func(**arguments)

    def get_tool_names(self) -> List[str]:
        """Get list of available tool names."""
        return list(self.wrappers.keys())
