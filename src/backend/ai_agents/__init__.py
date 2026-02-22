# AI Agents Package
# Note: Using ai_agents to avoid conflict with openai-agents-sdk

from .todo_agent import TodoAgent
from .cohere_provider import (
    setup_cohere_environment,
    configure_cohere_provider,
    get_cohere_api_key,
    COHERE_LITELLM_MODEL,
    create_cohere_agent_config,
    get_cohere_model_settings,
)

__all__ = [
    "TodoAgent",
    "setup_cohere_environment",
    "configure_cohere_provider",
    "get_cohere_api_key",
    "COHERE_LITELLM_MODEL",
    "create_cohere_agent_config",
    "get_cohere_model_settings",
]
