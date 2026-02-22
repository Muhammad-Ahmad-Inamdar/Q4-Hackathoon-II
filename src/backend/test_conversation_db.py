"""
Test script to verify conversation and message persistence in Neon DB.

This script tests:
1. Database connection to Neon DB
2. Creating a conversation
3. Saving messages
4. Retrieving conversation history
5. User isolation

Usage:
    python -m src.backend.test_conversation_db
    
Or from src/backend directory:
    python test_conversation_db.py
"""
import sys
import os
from datetime import datetime

# Add the src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlmodel import Session, select
from app.database import engine, create_tables
from app.models import Conversation, Message, User
from services.conversation_service import (
    get_or_create_conversation,
    save_message,
    get_conversation_history,
    get_user_conversations,
)
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def test_conversation_persistence():
    """Test conversation and message persistence in Neon DB"""
    
    print("=" * 60)
    print("CONVERSATION DB PERSISTENCE TEST")
    print("=" * 60)
    
    # Verify database connection
    print(f"\n1. Database Connection Test")
    print(f"   DATABASE_URL: {DATABASE_URL[:50]}...")
    
    if not DATABASE_URL or DATABASE_URL.startswith("sqlite"):
        print("   [WARN] Not using Neon DB - check .env file")
        return False
    
    print("   [OK] Using PostgreSQL (Neon DB)")
    
    # Create tables if needed
    print(f"\n2. Table Verification")
    create_tables()
    print("   [OK] Tables verified/created")
    
    # Test with a test user - create user first (required by FK constraint)
    test_user_id = "test_user_" + datetime.now().strftime("%Y%m%d%H%M%S")
    test_email = f"{test_user_id}@test.com"
    
    print(f"\n3. Create Test User")
    with Session(engine) as session:
        # Create test user
        test_user = User(
            id=test_user_id,
            email=test_email,
            password="test_password_hash"  # In real app, this would be hashed
        )
        session.add(test_user)
        session.commit()
        print(f"   [OK] Created test user: {test_user_id} ({test_email})")
    
    print(f"\n4. Create Conversation Test")
    print(f"   Test user ID: {test_user_id}")
    
    with Session(engine) as session:
        # Test get_or_create_conversation
        conversation = get_or_create_conversation(session, test_user_id)
        conversation_id = str(conversation.id)
        print(f"   [OK] Created conversation: {conversation_id}")
        
        # Verify conversation was saved
        stmt = select(Conversation).where(Conversation.id == conversation_id)
        saved_conv = session.exec(stmt).first()
        assert saved_conv is not None, "Conversation not persisted!"
        assert saved_conv.user_id == test_user_id, "User ID mismatch!"
        print(f"   [OK] Conversation persisted with user_id: {saved_conv.user_id}")
        
        print(f"\n5. Save Messages Test")
        # Save user message
        user_msg = save_message(
            session=session,
            conversation_id=conversation_id,
            role="user",
            content="Hello, can you help me create a task?"
        )
        print(f"   [OK] Saved user message: {user_msg.id}")
        
        # Save assistant response
        assistant_msg = save_message(
            session=session,
            conversation_id=conversation_id,
            role="assistant",
            content="Of course! I can help you create a task. What would you like to do?"
        )
        print(f"   [OK] Saved assistant message: {assistant_msg.id}")
        
        # Save another exchange
        user_msg2 = save_message(
            session=session,
            conversation_id=conversation_id,
            role="user",
            content="Create a task to buy groceries"
        )
        print(f"   [OK] Saved second user message: {user_msg2.id}")
        
        assistant_msg2 = save_message(
            session=session,
            conversation_id=conversation_id,
            role="assistant",
            content="I've created a task 'buy groceries' for you."
        )
        print(f"   [OK] Saved second assistant message: {assistant_msg2.id}")
        
        print(f"\n6. Retrieve Conversation History Test")
        history = get_conversation_history(session, conversation_id)
        print(f"   [OK] Retrieved {len(history)} messages")
        
        assert len(history) == 4, f"Expected 4 messages, got {len(history)}"
        print(f"   [OK] Message count verified")
        
        # Verify message order
        for i, msg in enumerate(history):
            print(f"   Message {i+1}: {msg.role} - {msg.content[:50]}...")
        
        # Verify chronological order
        for i in range(1, len(history)):
            assert history[i].created_at >= history[i-1].created_at, "Messages not in order!"
        print(f"   [OK] Message ordering verified (chronological)")
        
        print(f"\n7. User Isolation Test")
        # Create another user and conversation for isolation test
        other_user_id = "other_user_" + datetime.now().strftime("%Y%m%d%H%M%S")
        other_email = f"{other_user_id}@test.com"
        
        # Create other user
        other_user = User(
            id=other_user_id,
            email=other_email,
            password="test_password_hash"
        )
        session.add(other_user)
        session.commit()
        
        other_conv = get_or_create_conversation(session, other_user_id)
        
        # Verify user can only see their own conversations
        user_convs = get_user_conversations(session, test_user_id)
        print(f"   User {test_user_id} has {len(user_convs)} conversation(s)")
        
        other_convs = get_user_conversations(session, other_user_id)
        print(f"   User {other_user_id} has {len(other_convs)} conversation(s)")
        
        # Verify isolation
        user_conv_ids = [str(c.id) for c in user_convs]
        assert str(other_conv.id) not in user_conv_ids, "User isolation failed!"
        print(f"   [OK] User isolation verified - users cannot see each other's conversations")
        
        print(f"\n8. Get User Conversations Test")
        all_user_convs = get_user_conversations(session, test_user_id)
        print(f"   [OK] Retrieved {len(all_user_convs)} conversation(s) for user")
        
        session.commit()
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)
    print("\nSummary:")
    print("  - Database connection: OK")
    print("  - Table creation: OK")
    print("  - Conversation persistence: OK")
    print("  - Message persistence: OK")
    print("  - Message ordering: OK")
    print("  - User isolation: OK")
    print("\nNeon DB is properly configured for conversation storage!")
    
    return True


if __name__ == "__main__":
    try:
        success = test_conversation_persistence()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[FAIL] Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
