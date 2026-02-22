# Data Model: Phase-III Todo AI Chatbot Integration

**Date**: 2026-02-08
**Feature**: 007-ai-chatbot-integration
**Phase**: Phase 1 - Design

## Overview

This document defines the database schema extensions required for conversation persistence in the AI chatbot feature. The design follows stateless architecture principles with the database as the single source of truth.

---

## New Entities

### Conversation

Represents a chat session between a user and the AI chatbot.

**Table Name**: `conversations`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique conversation identifier |
| user_id | UUID | NOT NULL, FOREIGN KEY → users(id) | Owner of the conversation |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | When conversation was created |
| updated_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Last message timestamp |

**Indexes**:
- `idx_conversations_user_id` on `user_id` (for user's conversation list)
- `idx_conversations_created_at` on `created_at` (for chronological ordering)

**Constraints**:
- `user_id` must reference an existing user in `users` table
- `updated_at` must be >= `created_at`

**Relationships**:
- Belongs to: User (many-to-one)
- Has many: Messages (one-to-many)

---

### Message

Represents a single message within a conversation (user or assistant).

**Table Name**: `messages`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique message identifier |
| conversation_id | UUID | NOT NULL, FOREIGN KEY → conversations(id) ON DELETE CASCADE | Parent conversation |
| role | VARCHAR(20) | NOT NULL, CHECK (role IN ('user', 'assistant')) | Message sender role |
| content | TEXT | NOT NULL | Message text content |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | When message was sent |

**Indexes**:
- `idx_messages_conversation_id` on `conversation_id` (for conversation history queries)
- `idx_messages_created_at` on `created_at` (for chronological ordering)
- `idx_messages_conversation_created` on `(conversation_id, created_at)` (composite for optimal query performance)

**Constraints**:
- `conversation_id` must reference an existing conversation
- `role` must be either 'user' or 'assistant'
- `content` cannot be empty (length > 0)
- Messages are immutable (no updates after creation)

**Relationships**:
- Belongs to: Conversation (many-to-one)

---

## Existing Entities (Reference)

### User

**Table Name**: `users` (existing, no changes)

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | User identifier |
| email | VARCHAR | User email |
| password_hash | VARCHAR | Hashed password |
| created_at | TIMESTAMP | Account creation date |

**Relationships**:
- Has many: Conversations (one-to-many)
- Has many: Tasks (one-to-many, existing)

---

### Task

**Table Name**: `tasks` (existing, no changes)

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Task identifier |
| user_id | UUID | Task owner |
| title | VARCHAR(200) | Task title |
| description | TEXT | Task description |
| is_completed | BOOLEAN | Completion status |
| created_at | TIMESTAMP | Creation date |
| updated_at | TIMESTAMP | Last update date |

**Relationships**:
- Belongs to: User (many-to-one)

---

## Entity Relationships Diagram

```
┌─────────────┐
│    User     │
│  (existing) │
└──────┬──────┘
       │
       │ 1:N
       │
       ├─────────────────────────────┐
       │                             │
       │                             │
┌──────▼──────────┐          ┌──────▼──────┐
│  Conversation   │          │    Task     │
│     (new)       │          │ (existing)  │
└──────┬──────────┘          └─────────────┘
       │
       │ 1:N
       │
┌──────▼──────────┐
│    Message      │
│     (new)       │
└─────────────────┘
```

---

## Database Migration

### Migration File: `007_add_conversation_tables.sql`

```sql
-- Migration: Add conversation and message tables for AI chatbot
-- Feature: 007-ai-chatbot-integration
-- Date: 2026-02-08

BEGIN;

-- Create conversations table
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT conversations_updated_after_created CHECK (updated_at >= created_at)
);

-- Create indexes for conversations
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_created_at ON conversations(created_at);

-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL CHECK (LENGTH(content) > 0),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create indexes for messages
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at);

-- Add trigger to update conversations.updated_at when new message is added
CREATE OR REPLACE FUNCTION update_conversation_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE conversations
    SET updated_at = NEW.created_at
    WHERE id = NEW.conversation_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_conversation_timestamp
AFTER INSERT ON messages
FOR EACH ROW
EXECUTE FUNCTION update_conversation_timestamp();

COMMIT;
```

### Rollback Script: `007_rollback_conversation_tables.sql`

```sql
-- Rollback: Remove conversation and message tables
-- Feature: 007-ai-chatbot-integration

BEGIN;

-- Drop trigger and function
DROP TRIGGER IF EXISTS trigger_update_conversation_timestamp ON messages;
DROP FUNCTION IF EXISTS update_conversation_timestamp();

-- Drop tables (cascade will remove foreign key constraints)
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS conversations CASCADE;

COMMIT;
```

---

## SQLModel Definitions

### Conversation Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")
```

### Message Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, Literal

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", nullable=False)
    role: Literal["user", "assistant"] = Field(nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    conversation: Optional[Conversation] = Relationship(back_populates="messages")
```

---

## Query Patterns

### Fetch Conversation History (Stateless Context Rebuild)

```python
from sqlmodel import select, Session

def get_conversation_history(
    session: Session,
    conversation_id: UUID,
    user_id: UUID
) -> List[Message]:
    """
    Fetch all messages for a conversation in chronological order.
    Validates user ownership for security.
    """
    # Verify conversation belongs to user
    conversation = session.get(Conversation, conversation_id)
    if not conversation or conversation.user_id != user_id:
        raise ValueError("Conversation not found or access denied")

    # Fetch messages ordered by timestamp
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )

    messages = session.exec(statement).all()
    return messages
```

### Create New Conversation

```python
def create_conversation(session: Session, user_id: UUID) -> Conversation:
    """Create a new conversation for a user."""
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation
```

### Add Message to Conversation

```python
def add_message(
    session: Session,
    conversation_id: UUID,
    role: Literal["user", "assistant"],
    content: str
) -> Message:
    """Add a message to an existing conversation."""
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    return message
```

### Get User's Conversations

```python
def get_user_conversations(
    session: Session,
    user_id: UUID,
    limit: int = 50
) -> List[Conversation]:
    """Get user's recent conversations."""
    statement = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(limit)
    )

    conversations = session.exec(statement).all()
    return conversations
```

---

## Data Validation Rules

### Conversation
- `user_id` must exist in users table
- `updated_at` automatically updated when new message added (via trigger)
- Cannot be deleted if user is deleted (CASCADE handles cleanup)

### Message
- `conversation_id` must exist in conversations table
- `role` must be exactly 'user' or 'assistant' (case-sensitive)
- `content` cannot be empty string
- Messages are immutable (no UPDATE operations)
- Deleted when parent conversation is deleted (CASCADE)

---

## Performance Considerations

### Indexing Strategy
- **Primary queries**: Fetch messages by conversation_id (indexed)
- **Secondary queries**: List user's conversations (user_id indexed)
- **Composite index**: (conversation_id, created_at) optimizes history fetching

### Query Optimization
- Use connection pooling (10-20 connections)
- Limit conversation history to last 1000 messages if needed
- Consider read replicas for high-traffic scenarios
- Monitor query performance with EXPLAIN ANALYZE

### Storage Estimates
- Average message size: ~200 bytes (text content)
- 1000 messages per conversation: ~200 KB
- 1000 users × 10 conversations × 1000 messages: ~2 GB
- Neon Serverless PostgreSQL handles this scale efficiently

---

## Security Considerations

### User Isolation
- All queries MUST filter by user_id
- Conversation ownership validated before access
- Foreign key constraints enforce referential integrity

### Data Privacy
- Messages contain user-generated content (PII possible)
- Consider encryption at rest (Neon provides this)
- Implement data retention policy if required
- Sanitize logs to avoid exposing message content

---

## Testing Checklist

- [ ] Migration executes successfully on clean database
- [ ] Rollback script removes all tables and constraints
- [ ] Foreign key constraints prevent orphaned records
- [ ] Indexes improve query performance (verify with EXPLAIN)
- [ ] Trigger updates conversation.updated_at correctly
- [ ] SQLModel definitions match database schema
- [ ] Query patterns return correct results
- [ ] User isolation prevents cross-user data access
- [ ] Concurrent inserts don't cause race conditions

---

## Next Steps

1. ✅ Data model design complete
2. → Create API contracts (contracts/chat-api.yaml, contracts/mcp-tools.yaml)
3. → Create quickstart guide (quickstart.md)
4. → Execute database migration
5. → Implement SQLModel models in backend
