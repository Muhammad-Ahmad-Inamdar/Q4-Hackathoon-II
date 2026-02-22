---
name: tailwind-shadcn-ui
description: Build clean, consistent UI using TailwindCSS and shadcn/ui components.
---

# Tailwind + shadcn UI

## Instructions
1. **Component usage**
   - Prefer shadcn components
   - Customize via Tailwind classes
   - Avoid inline styles

2. **Design rules**
   - Consistent spacing (`gap-4`, `p-6`)
   - Use semantic colors
   - Mobile-first layout

3. **Reusability**
   - Extract common UI into components
   - Avoid page-specific styling

## Best Practices
- Use `cn()` utility for conditional classes
- Keep UI logic separate from business logic

## Example
```tsx
<Button variant="outline" className="w-full">
  Submit
</Button>
```
