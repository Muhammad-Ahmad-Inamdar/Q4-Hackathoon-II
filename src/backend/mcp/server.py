"""
MCP Server Setup for Phase-III Todo AI Chatbot.
Uses Official MCP SDK to expose task operation tools.
"""
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from mcp.shared.exceptions import McpError
import logging

# Import MCP tools
from .tools import (
    add_task_tool,
    list_tasks_tool,
    update_task_tool,
    complete_task_tool,
    delete_task_tool
)

# Configure logging
logger = logging.getLogger("mcp_server")

# Create MCP server instance
server = Server("todo-chatbot-mcp")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available MCP tools.
    These tools are exposed to the AI agent for task operations.
    """
    return [
        Tool(
            name="add_task",
            description="Create a new task for a user. Requires user_id and title. Description is optional.",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The UUID of the authenticated user"
                    },
                    "title": {
                        "type": "string",
                        "description": "The task title (max 255 characters)",
                        "minLength": 1,
                        "maxLength": 255
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description (max 1000 characters)",
                        "maxLength": 1000
                    }
                },
                "required": ["user_id", "title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="List tasks for a user. Can filter by status (all, pending, completed).",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The UUID of the authenticated user"
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter tasks by status",
                        "enum": ["all", "pending", "completed"],
                        "default": "all"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="update_task",
            description="Update a task's title and/or description. Requires user_id and task_id.",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The UUID of the authenticated user"
                    },
                    "task_id": {
                        "type": "string",
                        "description": "The UUID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "The new task title (max 255 characters)",
                        "minLength": 1,
                        "maxLength": 255
                    },
                    "description": {
                        "type": "string",
                        "description": "The new task description (max 1000 characters)",
                        "maxLength": 1000
                    }
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed. Requires user_id and task_id.",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The UUID of the authenticated user"
                    },
                    "task_id": {
                        "type": "string",
                        "description": "The UUID of the task to complete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Delete a task permanently. Requires user_id and task_id.",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The UUID of the authenticated user"
                    },
                    "task_id": {
                        "type": "string",
                        "description": "The UUID of the task to delete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool calls from the AI agent.
    Routes to the appropriate tool implementation.
    """
    logger.info(f"Tool call: {name} with arguments: {arguments}")

    try:
        if name == "add_task":
            result = add_task_tool(
                user_id=arguments.get("user_id"),
                title=arguments.get("title"),
                description=arguments.get("description")
            )
        elif name == "list_tasks":
            result = list_tasks_tool(
                user_id=arguments.get("user_id"),
                status=arguments.get("status", "all")
            )
        elif name == "update_task":
            result = update_task_tool(
                user_id=arguments.get("user_id"),
                task_id=arguments.get("task_id"),
                title=arguments.get("title"),
                description=arguments.get("description")
            )
        elif name == "complete_task":
            result = complete_task_tool(
                user_id=arguments.get("user_id"),
                task_id=arguments.get("task_id")
            )
        elif name == "delete_task":
            result = delete_task_tool(
                user_id=arguments.get("user_id"),
                task_id=arguments.get("task_id")
            )
        else:
            raise McpError(f"Unknown tool: {name}")

        logger.info(f"Tool call successful: {name}")
        return [TextContent(type="text", text=str(result))]

    except Exception as e:
        logger.error(f"Tool call failed: {name} - {str(e)}")
        raise McpError(f"Tool execution failed: {str(e)}")


async def run_server():
    """Run the MCP server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_server())
