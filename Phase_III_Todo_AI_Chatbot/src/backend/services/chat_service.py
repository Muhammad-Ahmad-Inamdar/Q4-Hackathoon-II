"""
Chat Service for Todo AI Chatbot

This service orchestrates chat requests using OpenAI Agents SDK with Cohere, handling:
1. Conversation retrieval/creation
2. AI agent invocation (OpenAI Agents SDK with Cohere via LiteLLM)
3. Message persistence
4. Response generation

Task IDs: T031-T035 (Chat Service Implementation with OpenAI Agents SDK)
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlmodel import Session, select

from services.conversation_service import (
    get_or_create_conversation,
    save_message,
    get_conversation_history,
)
from ai_agents.todo_agent import TodoAgent

logger = logging.getLogger(__name__)


class ChatService:
    """
    Service for processing chat requests using OpenAI Agents SDK.
    Stateless architecture - all state persisted to database.
    """

    def __init__(self, session: Session):
        """
        Initialize chat service.

        Args:
            session: Database session
        """
        self.session = session
        logger.info("ChatService initialized with OpenAI Agents SDK")

    def process_chat_request(
        self,
        user_id: str,
        message: str,
        cohere_api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a chat request from user using OpenAI Agents SDK with Cohere.

        Args:
            user_id: Authenticated user's ID
            message: User's natural language message
            cohere_api_key: Optional Cohere API key (defaults to COHERE_API_KEY env var)

        Returns:
            Dict with response, conversation_id, and metadata

        Flow:
        1. Get or create conversation
        2. Save user message to database
        3. Load conversation history
        4. Invoke AI agent (OpenAI Agents SDK with Cohere)
        5. Save assistant response to database
        6. Return response
        """
        try:
            logger.info(f"ChatService: Processing chat request for user {user_id}")

            # Step 1: Get or create conversation
            conversation = get_or_create_conversation(self.session, user_id)
            conversation_id = str(conversation.id)

            logger.info(f"ChatService: Using conversation {conversation_id}")

            # Step 2: Save user message to database
            save_message(
                session=self.session,
                conversation_id=conversation_id,
                role="user",
                content=message
            )

            logger.info(f"ChatService: Saved user message to conversation {conversation_id}")

            # Step 3: Load conversation history
            history = get_conversation_history(
                session=self.session,
                conversation_id=conversation_id,
                limit=20  # Last 20 messages for context
            )

            # Convert to format expected by TodoAgent
            conversation_history = [
                {"role": msg.role, "content": msg.content}
                for msg in history
            ]

            # Step 4: Invoke AI agent (OpenAI Agents SDK with Cohere)
            agent = TodoAgent(user_id=user_id, cohere_api_key=cohere_api_key)

            # Set agent's history from database
            agent.set_history_from_database(conversation_history)

            # Process the message
            agent_response = agent.process_message(message)

            # Add messages to agent's in-memory history for session context
            agent.add_to_history("user", message)
            agent.add_to_history("assistant", agent_response.get("response", ""))

            # Clean up agent resources
            agent.close()

            logger.info(f"ChatService: AI agent response received")

            # Step 5: Save assistant response to database
            response_text = agent_response.get("response", "I'm sorry, I couldn't process that.")

            save_message(
                session=self.session,
                conversation_id=conversation_id,
                role="assistant",
                content=response_text
            )

            logger.info(f"ChatService: Saved assistant response to conversation {conversation_id}")

            # Step 6: Return response
            return {
                "conversation_id": conversation_id,
                "response": response_text,
                "timestamp": datetime.utcnow().isoformat(),
                "intent": agent_response.get("intent"),
                "confidence": agent_response.get("confidence"),
            }

        except Exception as e:
            logger.error(f"ChatService: Error processing chat request: {str(e)}")
            raise

    def get_chat_history(
        self,
        user_id: str,
        conversation_id: Optional[str] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Get chat history for a user.

        Args:
            user_id: Authenticated user's ID
            conversation_id: Optional specific conversation ID
            limit: Maximum number of messages to return

        Returns:
            Dict with conversation and messages
        """
        try:
            from app.models import Conversation

            if conversation_id:
                # Get specific conversation
                statement = select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id
                )
                conversation = self.session.exec(statement).first()

                if not conversation:
                    return {
                        "success": False,
                        "error": "Conversation not found"
                    }

                # Get messages
                history = get_conversation_history(
                    session=self.session,
                    conversation_id=conversation_id,
                    limit=limit
                )

                return {
                    "success": True,
                    "conversation": {
                        "id": str(conversation.id),
                        "created_at": conversation.created_at.isoformat(),
                        "updated_at": conversation.updated_at.isoformat(),
                    },
                    "messages": [
                        {
                            "id": str(msg.id),
                            "role": msg.role,
                            "content": msg.content,
                            "created_at": msg.created_at.isoformat(),
                        }
                        for msg in history
                    ],
                }
            else:
                # Get all conversations for user with message count
                from sqlalchemy.orm import selectinload
                from sqlmodel import select
                
                # First get conversations
                statement = select(Conversation).where(
                    Conversation.user_id == user_id
                ).order_by(Conversation.updated_at.desc()).limit(10)

                conversations = self.session.exec(statement).all()
                
                # Get message counts separately (more efficient than loading all messages)
                from app.models import Message
                conversation_data = []
                for conv in conversations:
                    msg_count = self.session.exec(
                        select(Message.id).where(Message.conversation_id == str(conv.id))
                    ).all()
                    conversation_data.append({
                        "id": str(conv.id),
                        "created_at": conv.created_at.isoformat(),
                        "updated_at": conv.updated_at.isoformat(),
                        "message_count": len(msg_count),
                    })

                return {
                    "success": True,
                    "conversations": conversation_data,
                }

        except Exception as e:
            logger.error(f"ChatService: Error getting chat history: {str(e)}")
            return {
                "success": False,
                "error": str(e),
            }

    def clear_conversation(
        self,
        user_id: str,
        conversation_id: str
    ) -> Dict[str, Any]:
        """
        Clear all messages in a conversation.

        Args:
            user_id: Authenticated user's ID
            conversation_id: Conversation ID to clear

        Returns:
            Dict with success status
        """
        try:
            from app.models import Conversation, Message

            # Verify conversation belongs to user
            statement = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
            conversation = self.session.exec(statement).first()

            if not conversation:
                return {
                    "success": False,
                    "error": "Conversation not found"
                }

            # Delete all messages
            delete_statement = delete(Message).where(
                Message.conversation_id == conversation_id
            )
            self.session.exec(delete_statement)
            self.session.commit()

            logger.info(f"ChatService: Cleared conversation {conversation_id}")

            return {
                "success": True,
                "message": "Conversation cleared successfully"
            }

        except Exception as e:
            logger.error(f"ChatService: Error clearing conversation: {str(e)}")
            self.session.rollback()
            return {
                "success": False,
                "error": str(e),
            }


# Import needed for clear_conversation
from sqlmodel import delete
from app.models import Message
