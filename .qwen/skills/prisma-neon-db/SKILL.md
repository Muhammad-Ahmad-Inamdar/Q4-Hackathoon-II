---
name: prisma-neon-db
description: Manage PostgreSQL databases using Prisma ORM and Neon.
---

# Prisma + Neon Database

## Instructions
1. **Schema design**
   - Keep models minimal
   - Use relations wisely
   - Avoid premature optimization

2. **Migrations**
   - Always migrate, never edit DB manually
   - Use `prisma migrate dev`

3. **Queries**
   - Prefer server-side queries
   - Handle null cases

## Example
```ts
const users = await prisma.user.findMany();
```
