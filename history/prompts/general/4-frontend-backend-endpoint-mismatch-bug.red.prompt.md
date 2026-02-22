---
id: 4
title: "Frontend Backend Endpoint Mismatch Bug"
stage: red
date: 2026-01-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: "todo-app-phase-ii"
branch: "master"
user: "user"
command: "/sp.phr"
labels: ["bug", "debugging", "authentication", "api", "integration"]
links:
  spec: null
  plan: null
  ticket: "BUG-001"
  adr: null
  pr: null
files:
  - "src/frontend/lib/api.ts"
  - "src/backend/app/auth/router.py"
tests:
  - "src/backend/tests/test_auth.py"
prompt_text: |
  /sp.phr

  Document bug discovery:

  **Bug ID:** BUG-001
  **Date:** [Current Date]
  **Severity:** Critical
  **Status:** Identified

  **Issue:**
  - Frontend calls: POST /api/auth/register
  - Backend expects: POST /api/auth/signup (or different endpoint/method)
  - Error: 422 Unprocessable Entity, Method Not Allowed

  **User Impact:**
  - Users cannot sign up
  - Shows "[object Object],[object Object]" error message

  **Root Cause Analysis:**
  1. Endpoint mismatch between frontend and backend
  2. OR POST method not properly configured
  3. OR request body validation failing

  **Investigation Steps:**
  1. Check backend auth routes in src/backend/app/routes/
  2. Check frontend API client in src/frontend/lib/api.ts
  3. Verify main.py router configuration
  4. Check request/response body formats

  **Proposed Fix:**
  - Align endpoint names: Use /api/auth/signup consistently OR /api/auth/register consistently
  - Ensure POST method is properly defined
  - Verify Pydantic models match request body
  - Add proper error handling in frontend

  **Files Affected:**
  - src/frontend/lib/api.ts
  - src/backend/app/auth/router.py

response_text: |
  Identified and documented a critical bug where frontend and backend authentication endpoints are mismatched, preventing user registration.

outcome: "Critical bug identified where frontend calls POST /api/auth/register but backend expects different endpoint, causing user registration to fail."
evaluation: "Root cause is endpoint mismatch between frontend and backend. Investigation confirmed the API client and backend router need alignment."
---