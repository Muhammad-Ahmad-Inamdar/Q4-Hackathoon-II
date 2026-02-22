---
name: tool-reasoning
description: Determines which MCP tool(s) should be invoked based on detected intent and current conversation context.
---

# Tool Reasoning Skill

## Instructions
1. **Map intent to tools**
   - CREATE intent → add_task tool
   - LIST intent → list_tasks tool
   - UPDATE intent → update_task tool
   - COMPLETE intent → complete_task tool
   - DELETE intent → delete_task tool

2. **Check prerequisites**
   - Verify all required parameters are available
   - Identify missing data that needs clarification
   - Ensure user_id is present for all operations

3. **Plan tool sequence**
   - Single tool for simple operations
   - Multiple tools for complex operations (e.g., list then update)
   - Maintain logical ordering

4. **Validate tool availability**
   - Only select tools that exist in MCP server
   - Never hallucinate or invent tools
   - Use exact tool names from schema

5. **Generate invocation plan**
   - Tool name
   - Required parameters
   - Expected output
   - Error handling strategy

## Best Practices
- Always verify tool exists before planning invocation
- Chain tools only when necessary (avoid over-engineering)
- Pass user_id explicitly to every tool call
- Handle tool failures gracefully
- Log tool selection reasoning for debugging
