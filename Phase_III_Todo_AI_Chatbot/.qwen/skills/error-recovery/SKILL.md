---
name: error-recovery
description: Handles failures and edge cases gracefully during AI-driven task management.
---

# Error Recovery Skill

## Instructions
1. **Detect error type**
   - Tool execution failure
   - Missing required parameters
   - Invalid input data
   - Database/network errors
   - Permission/authorization errors

2. **Translate to user-friendly message**
   - Avoid technical stack traces
   - Explain what went wrong in plain language
   - Be honest but not alarming

3. **Suggest corrective action**
   - What the user can do to fix it
   - Alternative approaches if available
   - When to retry vs. when to give up

4. **Log error details**
   - Capture full error for debugging
   - Include context (user_id, tool, parameters)
   - Maintain error history for patterns

5. **Graceful degradation**
   - Offer partial functionality if possible
   - Don't crash the conversation
   - Maintain conversational flow

## Best Practices
- Never expose internal error messages to users
- Provide actionable guidance, not just "something went wrong"
- Distinguish between user errors and system errors
- Retry transient failures automatically (with limits)
- Escalate persistent errors to logging/monitoring
