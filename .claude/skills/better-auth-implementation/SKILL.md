---
name: better-auth-implementation
description: Implement authentication using Better Auth with session handling and providers.
---

# Better Auth Implementation

## Instructions
1. **Setup**
   - Configure Better Auth server-side
   - Use env variables correctly
   - Verify provider credentials

2. **Client usage**
   - Use `useSession()` hook
   - Handle loading & unauth states
   - Redirect after login

3. **Security**
   - Never expose secrets
   - Validate sessions server-side

## Common Issues
- Token mismatch
- Provider misconfiguration
- Callback URL errors

## Example
```ts
const { data: session, isLoading } = useSession();
```
