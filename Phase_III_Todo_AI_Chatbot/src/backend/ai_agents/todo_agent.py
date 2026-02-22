"""
Todo AI Agent for Natural Language Task Management

This is the main AI agent that orchestrates intent detection, tool execution,
and task management for the Todo AI Chatbot using OpenAI Agents SDK with Cohere.

Task IDs: T026-T030 (AI Agent Orchestration with OpenAI Agents SDK)
"""

import logging
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import asyncio
import json

from agents import Agent, Runner, ModelSettings
from ai_agents.cohere_provider import setup_cohere_environment, COHERE_LITELLM_MODEL
from mcp.tools import MCP_TOOLS
from mcp.tool_integration import ToolExecutor

logger = logging.getLogger(__name__)


class TodoAgent:
    """
    Main AI agent for todo management via natural language.

    This agent uses OpenAI Agents SDK with Cohere (via LiteLLM) to:
    1. Receive natural language messages from users
    2. Detect intent and extract entities
    3. Execute MCP tools for task operations
    4. Generate friendly responses

    The agent is stateless - all state is persisted to the database.
    """

    # Agent configuration
    AGENT_NAME = "Todo Assistant"
    AGENT_INSTRUCTIONS = """
You are a helpful Todo Management Assistant. Your role is to help users manage their tasks through natural conversation.

Available Actions (via tools):
- add_task: Create a new task with title and optional description
- list_tasks: Show user's tasks (can filter by status: all, pending, completed)
- update_task: Modify a task's title or description
- complete_task: Mark a task as completed
- delete_task: Remove a task permanently

Guidelines:
1. Always be friendly, encouraging, and concise
2. When a user wants to create a task, extract the title and description from their message
3. When listing tasks, present them in a clear, formatted way with emojis
4. For task modifications (update, complete, delete), ensure you have the task_id
5. If information is missing (e.g., task_id, title), ask clarifying questions
6. Never expose technical details, error codes, or internal tool names to users
7. Keep responses natural and conversational (1-3 sentences typically)
8. For list operations, summarize the results naturally

Examples:
- User: "Add a task to buy groceries" → Use add_task with title="Buy groceries"
- User: "Show me my pending tasks" → Use list_tasks with status="pending"
- User: "I finished task 123" → Use complete_task with task_id="123"
- User: "What do I need to do?" → Use list_tasks with status="pending"

Current User ID: {user_id}
"""

    def __init__(self, user_id: str, cohere_api_key: Optional[str] = None):
        """
        Initialize the Todo Agent with OpenAI Agents SDK.

        Args:
            user_id: Authenticated user's ID
            cohere_api_key: Optional Cohere API key (defaults to COHERE_API_KEY env var)
        """
        self.user_id = user_id
        self.cohere_api_key = cohere_api_key

        # Set up Cohere environment and get model
        self.model = setup_cohere_environment(api_key=cohere_api_key)

        # Create tool executor for MCP tools
        self.tool_executor = ToolExecutor(user_id=user_id, mcp_tools=MCP_TOOLS)

        # Build instructions with user context
        instructions = self.AGENT_INSTRUCTIONS.format(user_id=user_id)

        # Create the agent with OpenAI Agents SDK
        self.agent = Agent(
            name=self.AGENT_NAME,
            instructions=instructions,
            model=self.model,
            model_settings=ModelSettings(
                temperature=0.1,  # Low temperature for consistent behavior
                max_tokens=2048,
            ),
        )

        # Conversation history for context (stored in database, not in agent)
        self.conversation_history: List[Dict[str, str]] = []

        logger.info(f"TodoAgent initialized for user {user_id} with Cohere model")

    def process_message(self, message: str) -> Dict[str, Any]:
        """
        Process a user message and return AI response.

        This is the main entry point for processing user messages.

        Args:
            message: User's natural language message

        Returns:
            Dict with response, intent, confidence, and metadata

        Flow:
        1. Detect intent from message
        2. Extract entities for tool execution
        3. Execute MCP tool if applicable
        4. Generate response based on tool result
        5. Return structured response
        """
        try:
            logger.info(f"TodoAgent: Processing message from user {self.user_id}: '{message[:50]}...'")

            # Step 1: Detect intent and extract entities
            intent, entities = self._detect_intent_and_entities(message)

            logger.info(f"TodoAgent: Detected intent='{intent}'")

            # Step 2: Check if clarification needed
            clarification = self._check_clarification_needed(intent, entities, message)

            if clarification:
                response_text = clarification
                return {
                    "response": response_text,
                    "intent": intent,
                    "confidence": 0.5,
                    "clarification_requested": True,
                    "timestamp": datetime.utcnow().isoformat(),
                }

            # Step 3: Execute MCP tool if applicable
            tool_result = None
            tool_name = self._get_tool_for_intent(intent)

            if tool_name:
                tool_result = self._execute_tool(tool_name, entities)

            # Step 4: Generate response
            response_text = self._generate_response(intent, tool_result, entities, message)

            logger.info(f"TodoAgent: Generated response, length={len(response_text)}")

            return {
                "response": response_text,
                "intent": intent,
                "confidence": 0.9,
                "tool_executed": tool_name,
                "tool_result": tool_result,
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(f"TodoAgent: Error processing message: {str(e)}")
            error_response = "I encountered an error processing your request. Please try again."

            return {
                "response": error_response,
                "error": str(e),
                "intent": "error",
                "confidence": 0.0,
                "timestamp": datetime.utcnow().isoformat(),
            }

    def _detect_intent_and_entities(self, message: str) -> tuple:
        """
        Detect intent and extract entities from user message.

        Args:
            message: User's message

        Returns:
            Tuple of (intent, entities dict)
        """
        message_lower = message.lower()
        entities = {}
        intent = "general"

        # Check for get_task FIRST (more specific pattern)
        if any(word in message_lower for word in ["show task", "task details", "what is task", "task number", "get task"]):
            intent = "get_task"
            entities["task_id"] = self._extract_task_id(message)
            entities["task_reference"] = self._extract_task_reference(message)

        # Create task - look for creation keywords
        elif any(word in message_lower for word in ["add", "create", "new task", "need to", "want to", "remember to", "i have to", "i must"]):
            intent = "create_task"
            # Extract title from message
            entities["title"] = self._extract_task_title(message)

        # List tasks - look for listing/querying keywords (but not "show task")
        # Check this BEFORE complete_task to avoid "completed tasks" being detected as complete_task
        elif any(word in message_lower for word in ["show me", "list", "what are", "my tasks", "pending", "todo", "what do i", "what's on", "what is on", "view tasks", "get tasks", "all tasks", "completed tasks"]):
            intent = "list_tasks"
            # Check for status filter
            if "completed" in message_lower:
                entities["status"] = "completed"
            elif "pending" in message_lower or "incomplete" in message_lower:
                entities["status"] = "pending"
            else:
                entities["status"] = "all"

        # Complete task - look for completion keywords
        # Use more specific patterns to avoid false positives with "completed tasks"
        elif any(phrase in message_lower for phrase in ["mark as done", "mark done", "check off", "tick off", "i finished", "i completed"]) or \
             (any(word in message_lower for word in ["complete", "finish", "done", "accomplished", "marked"]) and "completed tasks" not in message_lower and "show completed" not in message_lower):
            intent = "complete_task"
            # Extract task ID or reference
            entities["task_id"] = self._extract_task_id(message)
            entities["task_reference"] = self._extract_task_reference(message)

        # Update task - look for modification keywords
        elif any(word in message_lower for word in ["update", "change", "edit", "modify", "rename", "alter", "set to"]):
            intent = "update_task"
            entities["task_id"] = self._extract_task_id(message)
            entities["task_reference"] = self._extract_task_reference(message)
            new_title = self._extract_task_title(message)
            if new_title:
                entities["title"] = new_title

        # Delete task - look for deletion keywords
        elif any(word in message_lower for word in ["delete", "remove", "cancel", "get rid", "erase", "drop", "clear"]):
            intent = "delete_task"
            entities["task_id"] = self._extract_task_id(message)
            entities["task_reference"] = self._extract_task_reference(message)

        return intent, entities

    def _extract_task_title(self, message: str) -> Optional[str]:
        """
        Extract task title from user message.

        Args:
            message: User's message

        Returns:
            Extracted title or None
        """
        # Simple extraction: look for text after common prefixes
        prefixes = ["add ", "create ", "new task: ", "task: ", "to "]

        message_lower = message.lower()
        for prefix in prefixes:
            if prefix in message_lower:
                idx = message_lower.find(prefix)
                title = message[idx + len(prefix):].strip()
                if title:
                    # Capitalize first letter
                    return title[0].upper() + title[1:] if len(title) > 1 else title.upper()

        # Fallback: return the whole message as title
        return message.strip() if len(message) < 100 else None

    def _extract_task_id(self, message: str) -> Optional[str]:
        """
        Extract task ID from user message.

        Args:
            message: User's message

        Returns:
            Extracted task ID or None
        """
        import re

        message_lower = message.lower()

        # Look for UUID pattern
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        match = re.search(uuid_pattern, message_lower)
        if match:
            return match.group()

        # Look for simple number pattern (task 1, task 123, etc.)
        number_pattern = r'task\s*(\d+)'
        match = re.search(number_pattern, message_lower)
        if match:
            # Note: This returns the number as string, actual ID resolution happens in tool
            return match.group(1)

        return None

    def _extract_task_reference(self, message: str) -> Optional[str]:
        """
        Extract task reference from user message (e.g., "first", "second", "last").

        This helps resolve ambiguous references like "delete the first task" or "complete the last one".

        Args:
            message: User's message

        Returns:
            Extracted reference (e.g., "first", "second", "last") or None
        """
        message_lower = message.lower()
        
        # Ordinal number patterns
        ordinals = {
            "first": "1",
            "second": "2", 
            "third": "3",
            "fourth": "4",
            "fifth": "5",
            "sixth": "6",
            "seventh": "7",
            "eighth": "8",
            "ninth": "9",
            "tenth": "10",
            "last": "last",
            "latest": "last",
            "most recent": "last",
            "previous": "previous",
            "previous one": "previous",
        }
        
        for ref, value in ordinals.items():
            if ref in message_lower:
                return value
        
        # Pattern for "the X task" where X is a number
        import re
        pattern = r'the\s+(\d+)(?:st|nd|rd|th)?\s*(?:task|one|it)'
        match = re.search(pattern, message_lower)
        if match:
            return match.group(1)
        
        return None

    def _check_clarification_needed(self, intent: str, entities: Dict, message: str) -> Optional[str]:
        """
        Check if clarification is needed before executing tool.

        Args:
            intent: Detected intent
            entities: Extracted entities
            message: Original message

        Returns:
            Clarification question or None
        """
        if intent == "create_task":
            if not entities.get("title"):
                return "What would you like to add as a task?"

        elif intent in ["complete_task", "update_task", "delete_task", "get_task"]:
            # Check if we have either a task_id or a task_reference
            has_task_id = entities.get("task_id") is not None
            has_reference = entities.get("task_reference") is not None
            
            if not has_task_id and not has_reference:
                return "Which task would you like to modify? Please provide the task ID or describe the task (e.g., 'the first task', 'task 1')."

        elif intent == "update_task":
            if not entities.get("title") and not entities.get("description"):
                return "What would you like to update about the task?"

        return None

    def _get_tool_for_intent(self, intent: str) -> Optional[str]:
        """
        Get the MCP tool name for an intent.

        Args:
            intent: Detected intent

        Returns:
            Tool name or None
        """
        intent_tool_map = {
            "create_task": "add_task",
            "list_tasks": "list_tasks",
            "complete_task": "complete_task",
            "update_task": "update_task",
            "delete_task": "delete_task",
            "get_task": "get_task",
        }
        return intent_tool_map.get(intent)

    def _execute_tool(self, tool_name: str, entities: Dict) -> Dict[str, Any]:
        """
        Execute an MCP tool with extracted entities.

        Args:
            tool_name: Name of the tool to execute
            entities: Extracted entities

        Returns:
            Tool execution result
        """
        logger.info(f"TodoAgent: Executing tool '{tool_name}' with entities: {entities}")

        # Prepare arguments
        args = {"user_id": self.user_id}
        
        # Handle task reference resolution for operations that need task_id
        if tool_name in ["complete_task", "update_task", "delete_task", "get_task"]:
            task_id = entities.get("task_id")
            task_reference = entities.get("task_reference")
            
            # If we have a reference instead of a direct ID, resolve it
            if task_reference and not task_id:
                resolved_id = self._resolve_task_reference(task_reference)
                if resolved_id:
                    args["task_id"] = resolved_id
                else:
                    return {
                        "success": False,
                        "error": "Could not find the task you're referring to. Please try again with a specific task ID."
                    }
            elif task_id:
                # Check if task_id is a number (needs resolution) or UUID
                if task_id.isdigit():
                    resolved_id = self._resolve_task_reference(task_id)
                    if resolved_id:
                        args["task_id"] = resolved_id
                    else:
                        return {
                            "success": False,
                            "error": f"Task number {task_id} not found. Please check your task list."
                        }
                else:
                    # It's a UUID, use directly
                    args["task_id"] = task_id
        
        args.update({k: v for k, v in entities.items() if k not in ["task_reference"]})

        # Execute the tool
        result = self.tool_executor.execute(tool_name, args)

        logger.info(f"TodoAgent: Tool '{tool_name}' executed: success={result.get('success')}")

        return result

    def _resolve_task_reference(self, reference: str) -> Optional[str]:
        """
        Resolve a task reference (e.g., "1", "first", "last") to an actual task ID.

        Args:
            reference: The reference to resolve

        Returns:
            The actual task ID (UUID) or None if not found
        """
        try:
            # Get all pending tasks for the user
            list_result = self.tool_executor.execute("list_tasks", {"user_id": self.user_id, "status": "pending"})
            
            if not list_result.get("success"):
                return None
            
            tasks = list_result.get("tasks", [])
            
            if not tasks:
                return None
            
            # Handle "last" reference
            if reference == "last":
                return tasks[-1].get("task_id")
            
            # Handle numeric reference (1-indexed)
            try:
                index = int(reference) - 1  # Convert to 0-indexed
                if 0 <= index < len(tasks):
                    return tasks[index].get("task_id")
                return None
            except (ValueError, TypeError):
                return None
                
        except Exception as e:
            logger.error(f"TodoAgent: Error resolving task reference: {str(e)}")
            return None

    def _generate_response(
        self,
        intent: str,
        tool_result: Optional[Dict],
        entities: Dict,
        message: str
    ) -> str:
        """
        Generate a friendly response based on tool execution result.

        Args:
            intent: Detected intent
            tool_result: Tool execution result
            entities: Extracted entities
            message: Original message

        Returns:
            Friendly response string
        """
        if not tool_result:
            # General conversation - use simple response
            return self._generate_general_response(message)

        success = tool_result.get("success", False)
        error = tool_result.get("error")

        if not success:
            return self._generate_error_response(intent, error)

        # Generate success response based on intent
        if intent == "create_task":
            title = entities.get("title", "the task")
            return f"✅ I've added '{title}' to your task list! What else would you like to do?"

        elif intent == "list_tasks":
            tasks = tool_result.get("tasks", [])
            count = len(tasks)

            if count == 0:
                status = entities.get("status", "all")
                if status == "completed":
                    return "🎉 You have no completed tasks yet. Keep working!"
                elif status == "pending":
                    return "📋 You have no pending tasks. Great job!"
                else:
                    return "📋 You have no tasks yet. Add your first task!"

            # Format tasks nicely
            status_filter = entities.get("status", "all")
            status_text = ""
            if status_filter == "pending":
                status_text = "pending "
            elif status_filter == "completed":
                status_text = "completed "

            response = f"📋 You have {count} {status_text}tasks:\n\n"
            for i, task in enumerate(tasks[:10], 1):  # Show max 10 tasks
                checkbox = "✅" if task.get("completed") else "⬜"
                title = task.get("title", "Untitled")
                task_id = task.get("task_id", "")
                response += f"{i}. {checkbox} {title} (ID: {task_id[:8]}...)\n"

            if count > 10:
                response += f"\n... and {count - 10} more tasks."

            return response

        elif intent == "complete_task":
            if tool_result.get("already_completed"):
                return "✅ This task is already marked as complete!"
            title = tool_result.get("title", "the task")
            return f"🎉 Great job! I've marked '{title}' as complete!"

        elif intent == "update_task":
            title = tool_result.get("title", "the task")
            return f"✅ I've updated '{title}' for you!"

        elif intent == "delete_task":
            message_text = tool_result.get("message", "Task deleted successfully!")
            return f"🗑️ {message_text}"

        elif intent == "get_task":
            task = tool_result.get("task")
            if task:
                title = task.get("title", "Untitled")
                description = task.get("description", "No description")
                status = "✅ Completed" if task.get("completed") else "⬜ Pending"
                created = task.get("created_at", "Unknown date")
                return f"📋 Task Details:\n\n**Title:** {title}\n**Description:** {description}\n**Status:** {status}\n**Created:** {created}"
            return "Task details retrieved successfully!"

        return "I've processed your request!"

    def _generate_general_response(self, message: str) -> str:
        """
        Generate response for general conversation.

        Args:
            message: User's message

        Returns:
            Friendly response
        """
        # Simple greeting detection
        message_lower = message.lower()

        if any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
            return "Hello! I'm your Todo Assistant. I can help you manage your tasks. What would you like to do?"

        if any(word in message_lower for word in ["thank", "thanks"]):
            return "You're welcome! Is there anything else I can help you with?"

        if any(word in message_lower for word in ["help", "what can you do"]):
            return "I can help you manage your tasks! You can:\n• Add new tasks\n• List your tasks\n• Mark tasks as complete\n• Update task details\n• Delete tasks\n\nJust tell me what you'd like to do!"

        # Default response
        return "I'm here to help you manage your tasks. You can ask me to add, list, complete, update, or delete tasks. What would you like to do?"

    def _generate_error_response(self, intent: str, error: Optional[str]) -> str:
        """
        Generate error response.

        Args:
            intent: Detected intent
            error: Error message

        Returns:
            Friendly error response
        """
        if error and "not found" in error.lower():
            return "I couldn't find that task. Please check the task ID and try again."

        if error and "required" in error.lower():
            return "I need a bit more information to complete that action. Could you provide more details?"

        return "I encountered an issue processing that request. Please try again or rephrase your request."

    def add_to_history(self, role: str, content: str):
        """
        Add a message to conversation history.

        Note: In the stateless architecture, the primary history is stored
        in the database. This in-memory history is for the current session only.

        Args:
            role: "user" or "assistant"
            content: Message content
        """
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
        })

        # Keep history manageable (last 20 messages)
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]

        logger.debug(f"TodoAgent: Added {role} message to history, total: {len(self.conversation_history)}")

    def set_history_from_database(self, history: List[Dict[str, str]]):
        """
        Set conversation history from database.

        Args:
            history: List of message dicts from database
        """
        self.conversation_history = [
            {"role": msg.get("role", "user"), "content": msg.get("content", "")}
            for msg in history[-20:]  # Last 20 messages
        ]
        logger.debug(f"TodoAgent: Loaded {len(self.conversation_history)} messages from database")

    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get the conversation history.

        Returns:
            List of message dictionaries
        """
        return self.conversation_history.copy()

    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
        logger.info(f"TodoAgent: Cleared conversation history for user {self.user_id}")

    def close(self):
        """Clean up resources."""
        logger.info(f"TodoAgent: Cleaned up resources for user {self.user_id}")
