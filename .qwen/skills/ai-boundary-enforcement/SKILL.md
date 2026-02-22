---
name: ai-boundary-enforcement
description: Prevents AI agents from exceeding defined system boundaries.
---

# AI Boundary Enforcement Skill

## Instructions
1. **Define allowed actions**
   - List all permitted operations
   - Specify allowed tools
   - Define data access scope
   - Set rate limits if applicable

2. **Implement guardrails**
   - Validate every action before execution
   - Check permissions and authorization
   - Enforce resource limits
   - Block disallowed operations

3. **Detect boundary violations**
   - Monitor for unauthorized tool calls
   - Flag attempts to access restricted data
   - Identify privilege escalation attempts
   - Log all violations

4. **Handle violations gracefully**
   - Reject with clear error message
   - Don't expose internal security details
   - Log for security review
   - Continue conversation safely

5. **Audit and review**
   - Regular review of boundary definitions
   - Update as system evolves
   - Test boundary enforcement regularly

## Best Practices
- Fail closed (deny by default)
- Make boundaries explicit in agent instructions
- Test boundary enforcement with adversarial inputs
- Log all boundary checks for audit
- Never trust AI to self-enforce boundaries
