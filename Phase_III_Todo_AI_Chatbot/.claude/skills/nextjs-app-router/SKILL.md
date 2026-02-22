---
name: nextjs-app-router
description: Build scalable Next.js apps using App Router, layouts, and server/client components. Use for all Next.js projects.
---

# Next.js App Router

## Instructions
1. **Folder structure**
   - Use `app/` directory
   - Separate routes by feature
   - Use `layout.tsx` for shared UI

2. **Server vs Client**
   - Default to Server Components
   - Use `"use client"` only when needed
   - Keep logic on server where possible

3. **Routing**
   - Use file-based routing
   - Group routes with `(auth)` or `(dashboard)`
   - Use `not-found.tsx` and `error.tsx`

## Best Practices
- Avoid heavy logic in client components
- Fetch data in server components
- Keep layouts thin and reusable

## Example
```tsx
app/dashboard/layout.tsx
app/dashboard/page.tsx
app/(auth)/login/page.tsx
```
