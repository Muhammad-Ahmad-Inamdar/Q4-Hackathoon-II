---
name: stateless-context-rebuild
description: Reconstructs AI context from persisted conversation history to support stateless server architecture.
---

# Stateless Context Rebuild Skill

## Instructions
1. **Fetch conversation history**
   - Retrieve all messages for the conversation_id
   - Order by timestamp (oldest first)
   - Include both user and assistant messages

2. **Convert to agent format**
   - Map database schema to AI message format
   - Preserve role (user/assistant)
   - Maintain exact message content
   - Keep chronological order

3. **Reconstruct context array**
   - Build message array: `[{role: "user", content: "..."}, {role: "assistant", content: "..."}]`
   - Ensure alternating roles where applicable
   - Include system messages if needed

4. **Validate reconstruction**
   - Verify message count matches database
   - Check for missing or duplicate messages
   - Ensure deterministic ordering

5. **Append new user message**
   - Add current user input to context
   - Ready for AI agent invocation

## Best Practices
- Never rely on in-memory state or caching
- Always fetch from database as single source of truth
- Ensure deterministic reconstruction (same input = same output)
- Handle empty conversation history gracefully
- Limit context window if conversation is very long
