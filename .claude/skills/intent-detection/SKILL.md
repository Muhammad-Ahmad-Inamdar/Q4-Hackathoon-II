---
name: intent-detection
description: Detects the user's underlying intent from natural language input. Maps free-form text to actionable intents such as create, list, update, complete, or delete tasks.
---

# Intent Detection Skill

## Instructions
1. **Analyze user message**
   - Read the full natural language input
   - Identify task-related keywords and phrases
   - Look for action verbs (add, create, show, list, update, delete, complete, mark)

2. **Map to primary intent**
   - CREATE: adding new tasks
   - LIST: viewing/showing tasks
   - UPDATE: modifying existing tasks
   - COMPLETE: marking tasks as done
   - DELETE: removing tasks
   - QUERY: asking questions about tasks

3. **Extract entities**
   - Task title/description
   - Due dates or time references
   - Priority indicators
   - Status keywords

4. **Assess confidence**
   - HIGH: clear, unambiguous intent
   - MEDIUM: likely intent with minor ambiguity
   - LOW: unclear or multiple possible intents

5. **Handle ambiguity**
   - Flag missing information
   - Identify when clarification is needed
   - Never assume intent without sufficient signal

## Best Practices
- Normalize variations and synonyms (e.g., "add" = "create" = "new")
- Consider conversation context for pronouns ("it", "that one")
- Do not execute actions during detection phase
- Return structured intent data, not natural language
- When uncertain, ask for clarification rather than guessing
