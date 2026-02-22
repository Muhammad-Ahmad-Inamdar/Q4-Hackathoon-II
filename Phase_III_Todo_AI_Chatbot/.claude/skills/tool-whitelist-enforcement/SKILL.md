---
name: tool-whitelist-enforcement
description: Restricts AI agents to approved MCP tools only.
---

# Tool Whitelist Enforcement Skill

## Instructions
1. **Maintain tool whitelist**
   - List all approved MCP tools
   - Document tool purpose and usage
   - Version the whitelist
   - Review regularly

2. **Validate tool calls**
   - Check tool name against whitelist
   - Reject calls to non-whitelisted tools
   - Validate tool exists in MCP server
   - Ensure tool signature matches schema

3. **Block unauthorized tools**
   - Prevent hallucinated tool calls
   - Stop attempts to use system commands
   - Block file system access outside tools
   - Prevent network calls outside tools

4. **Log enforcement actions**
   - Record all tool call attempts
   - Flag rejected calls
   - Track patterns of violations
   - Alert on suspicious behavior

5. **Update whitelist safely**
   - Require explicit approval for new tools
   - Test new tools before whitelisting
   - Document why each tool is allowed
   - Remove deprecated tools

## Best Practices
- Whitelist is the single source of truth
- Never allow dynamic tool discovery by AI
- Make whitelist explicit in agent configuration
- Test enforcement with invalid tool names
- Review whitelist violations regularly
