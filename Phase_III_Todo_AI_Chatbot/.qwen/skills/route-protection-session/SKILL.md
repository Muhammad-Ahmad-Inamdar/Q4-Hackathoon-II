---
name: route-protection-session
description: Protect routes and APIs using session-based auth and middleware.
---

# Route Protection & Sessions

## Instructions
1. **Middleware**
   - Protect dashboard routes
   - Redirect unauth users

2. **Server-side checks**
   - Validate session before DB access
   - Never trust client state

3. **Client UX**
   - Show loaders
   - Graceful redirects

## Example
```ts
if (!session) redirect("/login");
```
