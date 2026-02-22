"""
Cohere API Adapter for Todo AI Chatbot

This module handles all interactions with the Cohere API for natural language understanding.
Uses Cohere's command-r-plus model for intent detection and response generation.

Task IDs: T020-T025 (AI Agent Implementation)
"""

import os
import cohere
from typing import Dict, Any, List, Optional
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class CohereAdapter:
    """
    Adapter for Cohere API integration.
    Handles natural language understanding and response generation.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Cohere client.
        
        Args:
            api_key: Cohere API key (defaults to COHERE_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        
        if not self.api_key:
            logger.error("CohereAdapter: COHERE_API_KEY not found in environment")
            raise ValueError("COHERE_API_KEY is required")
        
        self.client = cohere.Client(self.api_key)
        self.model = "command-r-08-2024"  # Current stable model for reasoning and tool use

        logger.info(f"CohereAdapter initialized with model: {self.model}")
    
    def detect_intent(self, message: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Detect user intent from natural language message.
        
        Args:
            message: User's natural language message
            conversation_history: List of previous messages for context
        
        Returns:
            Dict with intent, confidence, and extracted entities
        """
        # Build prompt for intent detection
        history_context = ""
        if conversation_history:
            for msg in conversation_history[-5:]:  # Last 5 messages for context
                role = msg.get("role", "user")
                content = msg.get("content", "")
                history_context += f"{role}: {content}\n"
        
        prompt = f"""
Analyze this user message and extract their intent for task management.

{history_context}User: {message}

Available intents:
- create_task: Create a new task (keywords: add, create, new, need to, want to)
- list_tasks: View tasks (keywords: show, list, what are my, what do i need)
- complete_task: Mark task as done (keywords: complete, finish, done, mark as complete)
- update_task: Modify task (keywords: update, change, edit, rename)
- delete_task: Remove task (keywords: delete, remove, cancel)
- general: General conversation or unclear intent

Respond in JSON format:
{{
    "intent": "<intent_name>",
    "confidence": <0.0-1.0>,
    "entities": {{
        "title": "<task title if mentioned>",
        "task_id": "<task ID if mentioned>",
        "description": "<description if mentioned>",
        "status": "<all|pending|completed for list queries>"
    }},
    "clarification_needed": <true|false>,
    "clarification_question": "<question to ask if clarification needed>"
}}
"""
        
        try:
            response = self.client.chat(
                model=self.model,
                message=prompt,
                temperature=0.1,  # Low temperature for consistent extraction
            )
            
            # Parse response to extract JSON
            import json
            import re
            
            # Find JSON in response (might be wrapped in markdown)
            json_match = re.search(r'\{.*\}', response.text.strip(), re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                # Fallback: try to parse entire response
                result = json.loads(response.text)
            
            logger.info(f"CohereAdapter: Detected intent '{result.get('intent', 'unknown')}' with confidence {result.get('confidence', 0)}")
            
            return result
            
        except Exception as e:
            logger.error(f"CohereAdapter: Error detecting intent: {str(e)}")
            # Return fallback intent
            return {
                "intent": "general",
                "confidence": 0.5,
                "entities": {},
                "clarification_needed": True,
                "clarification_question": "I'm having trouble understanding. Could you rephrase that?"
            }
    
    def generate_response(self, intent: str, tool_result: Dict[str, Any], context: Dict[str, Any] = None) -> str:
        """
        Generate a friendly, natural language response based on tool execution result.
        """
        
        context_str = ""
        if context:
            context_str = f"Context: {context}\n"
        
        prompt = f"""
Generate a friendly, conversational response for this task management action.

{context_str}
Action: {intent}
Result: {tool_result}

Response guidelines:
- Be friendly and encouraging
- Keep it concise (1-3 sentences)
- Use natural language, not robotic
- For success: Confirm the action and offer next steps
- For errors: Be empathetic and suggest alternatives
- For list_tasks: Format the list nicely with emojis
- Never expose technical details or error codes

Respond with only the natural language response (no JSON, no explanations).
"""
        
        try:
            response = self.client.chat(
                model=self.model,
                message=prompt,
                temperature=0.7,  # Higher temperature for natural variation
            )
            
            response_text = response.text.strip()
            logger.info(f"CohereAdapter: Generated response for intent '{intent}'")
            
            return response_text
            
        except Exception as e:
            logger.error(f"CohereAdapter: Error generating response: {str(e)}")
            # Return fallback response
            return self._get_fallback_response(intent, tool_result)
    
    def _get_fallback_response(self, intent: str, tool_result: Dict[str, Any]) -> str:
        """
        Get a fallback response when AI generation fails.
        """
        fallbacks = {
            "create_task": "Task created successfully!" if tool_result.get("success") else "Failed to create task. Please try again.",
            "list_tasks": f"You have {tool_result.get('count', 0)} tasks." if tool_result.get("success") else "Failed to retrieve tasks.",
            "complete_task": "Task marked as complete!" if tool_result.get("success") else "Failed to complete task.",
            "update_task": "Task updated successfully!" if tool_result.get("success") else "Failed to update task.",
            "delete_task": "Task deleted successfully!" if tool_result.get("success") else "Failed to delete task.",
            "general": "I'm here to help you manage your tasks. What would you like to do?"
        }
        
        return fallbacks.get(intent, "I've processed your request.")
    
    def chat(self, message: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        General chat method for handling natural language conversations.
        """
        try:
            # Build conversation context
            chat_history = []
            if conversation_history:
                for msg in conversation_history[-10:]:  # Last 10 messages
                    chat_history.append({
                        "role": msg.get("role", "user"),
                        "message": msg.get("content", "")
                    })
            
            response = self.client.chat(
                model=self.model,
                message=message,
                chat_history=chat_history,
                temperature=0.7,
            )
            
            return {
                "response": response.text.strip(),
                "conversation_id": None,
            }
            
        except Exception as e:
            logger.error(f"CohereAdapter: Error in chat: {str(e)}")
            return {
                "response": "I'm having trouble responding right now. Please try again.",
                "error": str(e)
            }
    
    def close(self):
        """Close the Cohere client connection."""
        if hasattr(self, 'client') and hasattr(self.client, 'close'):
            self.client.close()
            logger.info("CohereAdapter: Client connection closed")
