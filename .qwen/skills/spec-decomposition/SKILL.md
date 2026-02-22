---
name: spec-decomposition
description: Breaks high-level requirements into clear, implementable components.
---

# Spec Decomposition Skill

## Instructions
1. **Read the full specification**
   - Understand the complete feature scope
   - Identify all requirements and constraints
   - Note dependencies and prerequisites

2. **Identify logical components**
   - Break into frontend, backend, database, AI layers
   - Separate concerns (auth, data, UI, logic)
   - Group related functionality

3. **Define component boundaries**
   - Clear inputs and outputs for each component
   - Minimal coupling between components
   - Well-defined interfaces

4. **Create implementation units**
   - Each unit should be independently testable
   - Size appropriately (not too large, not too granular)
   - Assign to appropriate agent/skill

5. **Document dependencies**
   - What must be built first
   - What can be built in parallel
   - External dependencies

## Best Practices
- One component = one clear responsibility
- Avoid premature optimization or over-engineering
- Keep decomposition aligned with agent capabilities
- Document assumptions and constraints
- Validate decomposition against acceptance criteria
