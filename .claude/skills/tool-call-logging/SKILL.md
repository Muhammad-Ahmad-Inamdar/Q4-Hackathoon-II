---
name: tool-call-logging
description: Captures all MCP tool invocations for debugging, auditing, and evaluation.
---

# Tool Call Logging Skill

## Instructions
1. **Log before invocation**
   - Tool name
   - Input parameters (sanitize sensitive data)
   - Timestamp
   - User context (user_id, conversation_id)

2. **Log after invocation**
   - Success/failure status
   - Output data (sanitize if needed)
   - Execution duration
   - Any errors or warnings

3. **Structure log entries**
   - Use consistent format (JSON recommended)
   - Include correlation IDs for tracing
   - Tag with severity level
   - Enable filtering and searching

4. **Sanitize sensitive data**
   - Remove passwords, tokens, secrets
   - Hash or mask PII if needed
   - Preserve enough context for debugging

5. **Store logs appropriately**
   - Separate storage from application DB
   - Implement retention policies
   - Enable log aggregation and analysis

## Best Practices
- Log every tool call without exception
- Include enough context to reproduce issues
- Never log raw secrets or credentials
- Use structured logging (not plain text)
- Enable log levels (debug, info, warn, error)
- Support hackathon review and evaluation visibility
