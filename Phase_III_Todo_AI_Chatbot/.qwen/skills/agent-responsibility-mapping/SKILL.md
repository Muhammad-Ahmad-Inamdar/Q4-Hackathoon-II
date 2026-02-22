---
name: agent-responsibility-mapping
description: Assigns responsibilities to the correct agent based on scope and capability.
---

# Agent Responsibility Mapping Skill

## Instructions
1. **Understand agent capabilities**
   - Review each agent's defined scope
   - Know what tools each agent has access to
   - Understand agent specializations

2. **Analyze task requirements**
   - What needs to be done
   - What domain knowledge is required
   - What tools/systems are involved

3. **Match task to agent**
   - Frontend work → frontend-chat-engineer
   - Backend API → chat-backend-engineer
   - Database schema → conversation-db-architect
   - MCP tools → mcp-tools-engineer
   - AI behavior → ai-chat-agent
   - Auth/security → auth-context-guard
   - Testing → ai-qa-tester
   - Orchestration → phase-iii-orchestrator

4. **Define clear boundaries**
   - One agent = one responsibility
   - No overlap between agents
   - Clear handoff points

5. **Document assignments**
   - Which agent owns what
   - What each agent delivers
   - How agents communicate

## Best Practices
- Never assign same responsibility to multiple agents
- Avoid agent confusion by clear scope definition
- Use orchestrator for cross-agent coordination
- Provide agents with complete context for their work
- Validate assignments against agent capabilities
