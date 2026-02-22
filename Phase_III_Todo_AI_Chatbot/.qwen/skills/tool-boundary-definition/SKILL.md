---
name: tool-boundary-definition
description: Clearly defines what logic belongs inside MCP tools versus AI agents.
---

# Tool Boundary Definition Skill

## Instructions
1. **MCP Tool responsibilities**
   - Data operations (CRUD)
   - Business logic enforcement
   - Validation and constraints
   - Deterministic transformations
   - Database interactions

2. **AI Agent responsibilities**
   - Intent detection
   - Natural language understanding
   - Tool selection and orchestration
   - Response generation
   - Conversation management

3. **Draw clear boundaries**
   - Tools = stateless, deterministic functions
   - Agents = stateful, conversational intelligence
   - Tools don't make decisions, agents do
   - Tools don't generate text, agents do

4. **Avoid boundary violations**
   - Don't put AI logic in tools
   - Don't put data operations in agents
   - Keep tools simple and focused
   - Keep agents flexible and intelligent

5. **Design interfaces**
   - Tools expose clear, typed APIs
   - Agents call tools with explicit parameters
   - No hidden coupling or assumptions

## Best Practices
- Tools should be usable by any agent (not agent-specific)
- Tools should be testable without AI
- Agents should work with any compliant tool
- Keep tools stateless and idempotent
- Document tool contracts explicitly
