---
name: api-error-handling
description: Standardize API error handling and responses across backend.
---

# API Error Handling

## Instructions
1. **Error format**
   - Consistent JSON structure
   - Meaningful messages
   - Correct HTTP codes

2. **Logging**
   - Log server errors
   - Never expose stack traces to client

3. **Client handling**
   - Show friendly messages
   - Retry where appropriate

## Example
```ts
return NextResponse.json(
  { error: "Unauthorized" },
  { status: 401 }
);
```
