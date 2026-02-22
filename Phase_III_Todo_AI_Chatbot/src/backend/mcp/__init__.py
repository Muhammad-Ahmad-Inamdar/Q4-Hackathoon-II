# MCP Package

from mcp.tools import (
    MCP_TOOLS,
    add_task_tool,
    list_tasks_tool,
    update_task_tool,
    complete_task_tool,
    delete_task_tool,
    get_tool_schema,
)

from mcp.tool_integration import (
    MCPToolWrapper,
    create_mcp_tool_wrappers,
    get_tools_for_agent,
    ToolExecutor,
)

__all__ = [
    "MCP_TOOLS",
    "add_task_tool",
    "list_tasks_tool",
    "update_task_tool",
    "complete_task_tool",
    "delete_task_tool",
    "get_tool_schema",
    "MCPToolWrapper",
    "create_mcp_tool_wrappers",
    "get_tools_for_agent",
    "ToolExecutor",
]
