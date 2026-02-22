---
name: stateless-db-operations
description: Ensures all database interactions are stateless and idempotent.
---

# Stateless DB Operations Skill

## Instructions
1. **Treat database as single source of truth**
   - Never cache data in memory
   - Always fetch fresh data from DB
   - No session state or global variables

2. **Design idempotent operations**
   - Same operation can be repeated safely
   - Use upsert patterns where appropriate
   - Handle duplicate requests gracefully

3. **Pass all context explicitly**
   - Include user_id in every query
   - No implicit context or assumptions
   - Self-contained operations

4. **Avoid side effects**
   - One operation = one clear outcome
   - No hidden state changes
   - Predictable behavior

5. **Handle concurrency**
   - Use database transactions where needed
   - Implement optimistic locking if required
   - Detect and handle race conditions

## Best Practices
- Every DB operation must be self-contained
- No reliance on previous requests or in-memory state
- Use database constraints to enforce data integrity
- Log all DB operations for auditability
- Test operations in isolation
