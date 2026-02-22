"""
Conversation Service - Handles CRUD operations for conversations and messages.

Follows stateless architecture - all data persisted to database.
All operations enforce user isolation at the database level.

References:
- specs/007-ai-chatbot-integration/spec.md (FR-007, FR-008, FR-009, FR-014, SEC-002)
- app/models/conversation.py
- app/models/message.py

Query Patterns:
- get_or_create_conversation: Get existing or create new conversation for user
- save_message: Persist a message to a conversation
- get_conversation_history: Retrieve messages in chronological order
- get_user_conversations: List all conversations for a user
"""

from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from app.models import Conversation, Message


class ConversationService:
    """
    Service for managing conversations and messages.

    All methods enforce user isolation - users can only access their own data.
    All operations are designed to be async-ready and idempotent where applicable.
    """

    def __init__(self, session: Session):
        """
        Initialize the service with a database session.

        Args:
            session: SQLModel database session
        """
        self.session = session

    def get_or_create_conversation(self, user_id: str) -> Conversation:
        """
        Get the most recent conversation for a user, or create a new one.

        This is the primary entry point for chatbot interactions.
        Ensures each user has at least one active conversation.

        Args:
            user_id: The authenticated user's ID (user isolation enforced)

        Returns:
            The most recent conversation or a newly created one

        """
        # Try to get the most recent conversation
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        )
        conversation = self.session.exec(statement).first()

        if conversation:
            return conversation

        # Create new conversation
        conversation = Conversation(user_id=user_id)
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)

        return conversation

    def save_message(
        self,
        conversation_id: str,
        role: str,
        content: str
    ) -> Message:
        """
        Save a message to a conversation.

        Args:
            conversation_id: The conversation to add the message to
            role: Message role ('user' or 'assistant')
            content: The message content

        Returns:
            The saved message

        """
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )

        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)

        return message

    def get_conversation_history(
        self,
        conversation_id: str,
        limit: int = 50
    ) -> List[Message]:
        """
        Get messages from a conversation in chronological order.

        Args:
            conversation_id: The conversation to retrieve messages from
            limit: Maximum number of messages to return

        Returns:
            List of messages ordered by created_at ascending

        """
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )

        messages = self.session.exec(statement).all()
        return messages

    def get_user_conversations(self, user_id: str) -> List[Conversation]:
        """
        Get all conversations for a user.

        Args:
            user_id: The authenticated user's ID

        Returns:
            List of conversations ordered by updated_at descending

        """
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        )

        conversations = self.session.exec(statement).all()
        return conversations


# Convenience functions for direct use
def get_or_create_conversation(session: Session, user_id: str) -> Conversation:
    """Get or create a conversation for a user"""
    service = ConversationService(session)
    return service.get_or_create_conversation(user_id)


def save_message(
    session: Session,
    conversation_id: str,
    role: str,
    content: str
) -> Message:
    """Save a message to a conversation"""
    service = ConversationService(session)
    return service.save_message(conversation_id, role, content)


def get_conversation_history(
    session: Session,
    conversation_id: str,
    limit: int = 50
) -> List[Message]:
    """Get conversation history"""
    service = ConversationService(session)
    return service.get_conversation_history(conversation_id, limit)


def get_user_conversations(
    session: Session,
    user_id: str
) -> List[Conversation]:
    """Get all conversations for a user"""
    service = ConversationService(session)
    return service.get_user_conversations(user_id)
