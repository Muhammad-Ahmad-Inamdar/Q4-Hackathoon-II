"""
Chat API Endpoint for Todo AI Chatbot

REST API endpoint for chat interactions.
POST /api/{user_id}/chat

Task IDs: T036-T040 (Chat API Implementation)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
from typing import Dict, Any
import logging
import os

from app.database import get_session
from services.chat_service import ChatService
from app.auth.middleware import JWTBearer

logger = logging.getLogger(__name__)

chat_router = APIRouter()


@chat_router.post("/{user_id}/chat", response_model=Dict[str, Any])
def chat_request(
    user_id: str,
    request_body: Dict[str, str],
    request: Request,
    session: Session = Depends(get_session),
    token: str = Depends(JWTBearer())
):
    """
    Process a chat message from authenticated user.
    
    Args:
        user_id: Authenticated user's ID (from JWT token)
        request_body: Dict with "message" key containing user's message
        request: FastAPI request object
        session: Database session
        token: JWT token (validated by middleware)
    
    Returns:
        Dict with:
        - conversation_id: UUID of the conversation
        - response: AI assistant's response
        - timestamp: Response timestamp
        - intent: Detected intent (optional)
        - confidence: Intent confidence score (optional)
    
    Example Request:
        POST /api/user-123/chat
        {
            "message": "Add buy groceries to my todo list"
        }
    
    Example Response:
        {
            "conversation_id": "abc-123-def",
            "response": "Great! I've added 'Buy groceries' to your todo list.",
            "timestamp": "2026-02-17T12:00:00",
            "intent": "create_task",
            "confidence": 0.95
        }
    """
    try:
        # Validate user_id matches token
        token_user_id = getattr(request.state, "user_id", None)
        
        if not token_user_id:
            logger.warning("Chat endpoint: User ID not found in request state")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not authenticated"
            )
        
        if token_user_id != user_id:
            logger.warning(f"Chat endpoint: User ID mismatch - token: {token_user_id}, request: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID mismatch"
            )
        
        # Extract message from request body
        message = request_body.get("message", "").strip()
        
        if not message:
            logger.warning(f"Chat endpoint: Empty message from user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message is required"
            )
        
        # Validate message length
        if len(message) > 2000:
            logger.warning(f"Chat endpoint: Message too long from user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message must be 2000 characters or less"
            )
        
        logger.info(f"Chat endpoint: Processing message from user {user_id}: '{message[:50]}...'")
        
        # Get Cohere API key from environment
        cohere_api_key = os.getenv("COHERE_API_KEY")
        
        if not cohere_api_key:
            logger.error("Chat endpoint: COHERE_API_KEY not configured")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI service not configured"
            )
        
        # Process chat request
        chat_service = ChatService(session=session)
        
        response = chat_service.process_chat_request(
            user_id=user_id,
            message=message,
            cohere_api_key=cohere_api_key
        )
        
        logger.info(f"Chat endpoint: Successfully processed chat for user {user_id}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat endpoint: Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat request: {str(e)}"
        )


@chat_router.get("/{user_id}/chat/history")
def get_chat_history(
    user_id: str,
    request: Request,
    conversation_id: str = None,
    limit: int = 50,
    session: Session = Depends(get_session),
    token: str = Depends(JWTBearer())
):
    """
    Get chat history for authenticated user.
    
    Args:
        user_id: Authenticated user's ID
        conversation_id: Optional specific conversation ID
        limit: Maximum messages to return
        request: FastAPI request object
        session: Database session
        token: JWT token
    
    Returns:
        Dict with conversation(s) and messages
    """
    try:
        # Validate user_id
        token_user_id = getattr(request.state, "user_id", None)
        
        if not token_user_id or token_user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID mismatch"
            )
        
        # Get chat history
        chat_service = ChatService(session=session)
        history = chat_service.get_chat_history(
            user_id=user_id,
            conversation_id=conversation_id,
            limit=limit
        )
        
        return history
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat endpoint: Error getting chat history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get chat history: {str(e)}"
        )
