"""
Logger utility for Phase-III chatbot.
Provides structured logging for tool calls, errors, and conversation events.
"""
import logging
import sys
import os
from datetime import datetime
from typing import Optional

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Create logs directory
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Create logger
logger = logging.getLogger("phaseiii_chatbot")
logger.setLevel(getattr(logging, LOG_LEVEL.upper()))

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(getattr(logging, LOG_LEVEL.upper()))
console_formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# File handler
log_file = os.path.join(LOG_DIR, f"chatbot_{datetime.now().strftime('%Y%m%d')}.log")
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(getattr(logging, LOG_LEVEL.upper()))
file_formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def log_tool_call(
    tool_name: str,
    user_id: str,
    input_params: dict,
    output: Optional[dict] = None,
    error: Optional[str] = None
):
    """Log an MCP tool invocation."""
    log_data = {
        "event": "tool_call",
        "tool_name": tool_name,
        "user_id": user_id,
        "input": input_params,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if output:
        log_data["output"] = output
    
    if error:
        log_data["error"] = error
        logger.error(f"TOOL_CALL_FAILED: {log_data}")
    else:
        logger.info(f"TOOL_CALL: {log_data}")


def log_conversation_event(
    event_type: str,
    user_id: str,
    conversation_id: Optional[str] = None,
    message_id: Optional[str] = None,
    details: Optional[dict] = None
):
    """Log a conversation-related event."""
    log_data = {
        "event": "conversation_event",
        "event_type": event_type,
        "user_id": user_id,
        "conversation_id": conversation_id,
        "message_id": message_id,
        "details": details or {},
        "timestamp": datetime.utcnow().isoformat()
    }
    logger.info(f"CONVERSATION: {log_data}")


def log_agent_intent(
    user_id: str,
    user_message: str,
    detected_intent: str,
    selected_tool: Optional[str] = None
):
    """Log AI agent intent detection and tool selection."""
    log_data = {
        "event": "agent_intent",
        "user_id": user_id,
        "user_message": user_message,
        "detected_intent": detected_intent,
        "selected_tool": selected_tool,
        "timestamp": datetime.utcnow().isoformat()
    }
    logger.info(f"AGENT_INTENT: {log_data}")


def log_error(
    error_type: str,
    message: str,
    user_id: Optional[str] = None,
    stack_trace: Optional[str] = None
):
    """Log an error with context."""
    log_data = {
        "event": "error",
        "error_type": error_type,
        "message": message,
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if stack_trace:
        log_data["stack_trace"] = stack_trace
    
    logger.error(f"ERROR: {log_data}")


# Export logger for direct use
__all__ = ["logger", "log_tool_call", "log_conversation_event", "log_agent_intent", "log_error"]
