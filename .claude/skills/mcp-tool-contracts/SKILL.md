---
name: mcp-tool-contracts
description: Enforces strict adherence to MCP tool input and output schemas.
---

# MCP Tool Contracts Skill

## Instructions
1. **Define tool schema**
   - Input parameters (name, type, required/optional)
   - Output structure (success/error format)
   - Error codes and messages
   - Example usage

2. **Validate inputs**
   - Check all required parameters are present
   - Verify parameter types match schema
   - Validate value constraints (e.g., string length, number ranges)
   - Reject invalid inputs with clear error

3. **Ensure deterministic outputs**
   - Same input → same output (always)
   - No randomness or time-dependent behavior
   - Consistent error messages
   - Predictable data structures

4. **Maintain schema consistency**
   - Version tool schemas explicitly
   - Document breaking changes
   - Provide migration guides for schema updates
   - Never silently change contracts

5. **Test contract compliance**
   - Unit test all input/output combinations
   - Validate edge cases
   - Ensure error paths are covered

## Best Practices
- Document schemas in code and external docs
- Use TypeScript/JSON Schema for validation
- Fail fast on invalid inputs (don't guess)
- Never allow schema drift between versions
- Make breaking changes explicit and versioned
