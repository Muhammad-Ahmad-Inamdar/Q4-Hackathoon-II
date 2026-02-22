---
name: conversation-persistence
description: Manages storage and retrieval of conversations and messages.
---

# Conversation Persistence Skill

## Instructions
1. **Create conversation**
   - Generate unique conversation_id
   - Associate with user_id
   - Store metadata (created_at, title if applicable)
   - Return conversation_id for future reference

2. **Store messages**
   - Save each message with role (user/assistant)
   - Include timestamp for ordering
   - Link to conversation_id and user_id
   - Preserve exact content

3. **Retrieve conversation history**
   - Fetch all messages for conversation_id
   - Order chronologically (oldest first)
   - Filter by user_id for security
   - Return in consistent format

4. **Maintain message ordering**
   - Use timestamps or sequence numbers
   - Ensure deterministic retrieval order
   - Handle concurrent message writes

5. **Implement data retention**
   - Define retention policies
   - Archive or delete old conversations
   - Respect user privacy preferences

## Best Practices
- Always validate user_id matches conversation ownership
- Use database transactions for multi-message operations
- Index on conversation_id and user_id for performance
- Store messages immutably (no edits after creation)
- Implement soft deletes for audit trail
