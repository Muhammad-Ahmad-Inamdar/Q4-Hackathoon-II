---
name: deterministic-behavior-enforcer
description: Enforces predictable AI behavior for reproducibility and testing.
---

# Deterministic Behavior Enforcer Skill

## Instructions
1. **Eliminate randomness**
   - Use fixed seeds for any random operations
   - Avoid time-dependent behavior
   - Remove non-deterministic algorithms
   - Ensure consistent ordering

2. **Standardize outputs**
   - Use consistent response formats
   - Maintain stable message structures
   - Avoid creative variations in confirmations
   - Keep error messages predictable

3. **Control AI parameters**
   - Set temperature to 0 or very low
   - Use deterministic sampling
   - Disable random features
   - Configure for consistency

4. **Test reproducibility**
   - Same input → same output (always)
   - Run tests multiple times
   - Verify consistency across runs
   - Detect and fix non-determinism

5. **Document behavior**
   - Specify expected outputs for inputs
   - Define exact response patterns
   - List all decision rules
   - Make behavior predictable

## Best Practices
- Prioritize consistency over creativity
- Make AI behavior testable and verifiable
- Avoid "personality" that introduces variance
- Use structured outputs over free-form text
- Test determinism with automated checks
- Document any intentional non-determinism
