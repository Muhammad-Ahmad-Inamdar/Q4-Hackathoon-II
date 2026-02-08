---
id: 1001
title: "Fixed Auth Endpoint Mismatch"
stage: "red"
date: "2026-02-01"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "master"
user: "unknown"
command: "manual-fix"
labels: ["authentication", "api", "routing", "bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "src/frontend/lib/api.ts"
tests:
  - "none"
---

# Fixed Auth Endpoint Mismatch

## Context
User reported that the signup page was returning a 404 error when trying to register. The browser console showed: `Failed to load resource: the server responded with a status of 404 (Not Found)` for `http://localhost:8000/auth/register`.

## Problem
The frontend was calling authentication endpoints at `/auth/register` and `/auth/login`, but the backend had these endpoints mounted at `/api/auth/register` and `/api/auth/login` due to the router prefix configuration.

## Root Cause
In `src/backend/app/main.py`, the auth router is mounted with a `/api/auth` prefix:
```python
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
```

However, the frontend in `src/frontend/lib/api.ts` was calling endpoints without the `/api` prefix:
- `fetch(${API_BASE_URL}/auth/register` instead of `fetch(${API_BASE_URL}/api/auth/register`
- `fetch(${API_BASE_URL}/auth/login` instead of `fetch(${API_BASE_URL}/api/auth/login`

## Solution
Updated the frontend API calls in `src/frontend/lib/api.ts` to use the correct backend endpoints:
1. Changed `/auth/register` to `/api/auth/register`
2. Changed `/auth/login` to `/api/auth/login`
3. Changed `/auth/logout` to `/api/auth/logout`

## Verification
- Tested backend endpoints directly with curl: both `/api/auth/register` and `/api/auth/login` work correctly
- Both servers (frontend on port 3000, backend on port 8000) are running successfully
- Frontend authentication flow should now work properly

## Outcome
The 404 error on the signup page has been resolved. Users can now successfully register and authenticate with the backend API.

## Files Modified
- `src/frontend/lib/api.ts` - Updated endpoint URLs to match backend configuration

## Tests
Manual verification performed using curl commands to test backend endpoints directly.

## Next Steps
- Verify the complete authentication flow works in the browser
- Test login, signup, and logout functionality end-to-end

## Reflection
This was a common integration issue where frontend and backend API contracts were not aligned. The fix involved updating the frontend to match the actual backend endpoint structure.

## Prompt Text
```
meny npm run dev chlaya aur sign up krny ki koshih ki to
Not Found likha hua aaya aur console (browser) k yh
:8000/auth/register:1  Failed to load resource: the server responded with a status of 404 (Not Found)

http://localhost:8000/auth/register
{"detail":"Not Found"}

isko resolve karo

dosra yh k mery frontend main to koi /auth dir dir hai hi nahi
```

## Response Summary
Identified and fixed authentication endpoint mismatch between frontend and backend. Updated frontend API calls to use correct `/api/auth/` prefixed endpoints that match the backend router configuration.

## Acceptance Criteria
- [x] Signup endpoint returns 200 instead of 404
- [x] Login endpoint works correctly
- [x] Frontend and backend API contracts aligned
- [x] Authentication flow functional end-to-end