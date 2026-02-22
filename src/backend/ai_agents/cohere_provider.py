"""
Cohere Provider for OpenAI Agents SDK

This module configures the OpenAI Agents SDK to use Cohere API via LiteLLM.
The OpenAI Agents SDK supports non-OpenAI models through LiteLLM integration.

Task IDs: T020-T025 (AI Agent Implementation with OpenAI Agents SDK)
"""

import os
import logging
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Cohere model configuration
COHERE_MODEL_NAME = "cohere/command-r-08-2024"
COHERE_LITELLM_MODEL = f"litellm/{COHERE_MODEL_NAME}"

# Environment variable for Cohere API key
COHERE_API_KEY_ENV = "COHERE_API_KEY"


def get_cohere_api_key(api_key: Optional[str] = None) -> str:
    """
    Get Cohere API key from parameter or environment.

    Args:
        api_key: Optional API key parameter

    Returns:
        Cohere API key

    Raises:
        ValueError: If no API key is provided
    """
    key = api_key or os.getenv(COHERE_API_KEY_ENV)

    if not key:
        logger.error(f"CohereProvider: {COHERE_API_KEY_ENV} not found in environment")
        raise ValueError(f"{COHERE_API_KEY_ENV} is required for Cohere provider")

    return key


def configure_cohere_provider(api_key: Optional[str] = None) -> str:
    """
    Configure the OpenAI Agents SDK to use Cohere via LiteLLM.

    This function:
    1. Sets the Cohere API key in environment for LiteLLM
    2. Disables OpenAI tracing (since we're not using OpenAI)
    3. Sets default API to chat_completions (Responses API not supported by Cohere)
    4. Returns the model string to use with Agents SDK

    Args:
        api_key: Optional Cohere API key (defaults to COHERE_API_KEY env var)

    Returns:
        Model string for use with OpenAI Agents SDK (e.g., "litellm/cohere/command-r-08-2024")

    Example:
        ```python
        from agents import Agent, Runner, set_tracing_disabled
        from agents.cohere_provider import configure_cohere_provider

        # Configure Cohere provider
        model = configure_cohere_provider()

        # Create agent with Cohere model
        agent = Agent(
            name="Todo Assistant",
            instructions="You are a helpful todo management assistant.",
            model=model,
        )
        ```
    """
    # Get and set API key
    key = get_cohere_api_key(api_key)
    os.environ[COHERE_API_KEY_ENV] = key

    logger.info(f"CohereProvider: Configured with model '{COHERE_LITELLM_MODEL}'")

    return COHERE_LITELLM_MODEL


def get_cohere_model_settings(
    temperature: float = 0.1,
    max_tokens: int = 2048,
    top_p: float = 0.9,
) -> dict:
    """
    Get recommended model settings for Cohere.

    Args:
        temperature: Sampling temperature (0.0-1.0)
        max_tokens: Maximum tokens to generate
        top_p: Nucleus sampling parameter

    Returns:
        Dict with model settings compatible with OpenAI Agents SDK
    """
    return {
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
    }


def create_cohere_agent_config(
    name: str = "Todo Assistant",
    instructions: str = "You are a helpful todo management assistant.",
    temperature: float = 0.1,
    max_tokens: int = 2048,
    api_key: Optional[str] = None,
) -> dict:
    """
    Create a configuration dict for creating an Agent with Cohere.

    Args:
        name: Agent name
        instructions: System instructions for the agent
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        api_key: Optional Cohere API key

    Returns:
        Dict with agent configuration including model and settings

    Example:
        ```python
        from agents import Agent
        from agents.cohere_provider import create_cohere_agent_config

        config = create_cohere_agent_config(
            name="Todo Assistant",
            instructions="Help users manage their tasks.",
        )

        agent = Agent(**config)
        ```
    """
    model = configure_cohere_provider(api_key)

    return {
        "name": name,
        "instructions": instructions,
        "model": model,
        "model_settings": get_cohere_model_settings(
            temperature=temperature,
            max_tokens=max_tokens,
        ),
    }


def setup_cohere_environment(api_key: Optional[str] = None, disable_tracing: bool = True):
    """
    Set up the environment for using Cohere with OpenAI Agents SDK.

    This should be called once at application startup.

    Args:
        api_key: Optional Cohere API key
        disable_tracing: Whether to disable OpenAI tracing (default True for non-OpenAI)

    Returns:
        Model string for use with Agents SDK
    """
    # Configure Cohere provider
    model = configure_cohere_provider(api_key)

    # Disable tracing if not using OpenAI
    if disable_tracing:
        try:
            from agents import set_tracing_disabled
            set_tracing_disabled(True)
            logger.info("CohereProvider: Tracing disabled")
        except ImportError:
            logger.warning("CohereProvider: Could not disable tracing (agents module not available)")

    # Set default API to chat_completions (Responses API not supported by Cohere)
    try:
        from agents import set_default_openai_api
        set_default_openai_api("chat_completions")
        logger.info("CohereProvider: Set default API to chat_completions")
    except ImportError:
        logger.warning("CohereProvider: Could not set default API (agents module not available)")

    return model
