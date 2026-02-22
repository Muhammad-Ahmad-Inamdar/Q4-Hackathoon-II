---
name: requirement-to-behavior-mapping
description: Translates written requirements into observable system behavior.
---

# Requirement to Behavior Mapping Skill

## Instructions
1. **Extract requirements**
   - Read specification thoroughly
   - Identify functional requirements
   - Note non-functional requirements (performance, security)
   - List constraints and assumptions

2. **Define observable behaviors**
   - What the system should do (actions)
   - What the system should return (outputs)
   - How the system should respond to errors
   - Performance characteristics

3. **Create behavior scenarios**
   - Given [context]
   - When [action]
   - Then [expected outcome]
   - Use concrete examples

4. **Map to system components**
   - Which component implements this behavior
   - What interfaces are involved
   - What data flows through the system

5. **Validate completeness**
   - Every requirement has observable behavior
   - Every behavior is testable
   - Edge cases are covered

## Best Practices
- Use concrete, measurable behaviors (not vague descriptions)
- Include both happy path and error scenarios
- Make behaviors independently verifiable
- Avoid implementation details in behavior descriptions
- Ensure behaviors align with user value
