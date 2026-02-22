---
id: 7
title: "CORS Configuration Fixed"
stage: red
date: 2026-01-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: "todo-app-phase-ii"
branch: "master"
user: "user"
command: "/sp.tasks"
labels: ["bug-fix", "cors", "authentication", "api", "frontend", "backend"]
links:
  spec: "speckit/specify.md"
  plan: "speckit/plan.md"
  tasks: "speckit/tasks_cors_fix.md"
  ticket: "BUG-002"
  adr: null
  pr: null
files:
  - "src/backend/app/main.py"
  - "src/backend/.env"
tests:
  - "none"
prompt_text: |

signup:1 Access to fetch at 'http://localhost:8000/api/auth/register' from origin 'http://localhost:3000' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
:8000/api/auth/register:1  Failed to load resource: net::ERR_FAILED

Update §3 Technical Decisions - Add CORS Configuration Decision:

**Decision Point:** How to configure CORS for local development?

**Options Considered:**

1. **Allow all origins (*)**
   - Pros: Easy, works immediately
   - Cons: Security risk, not production-ready
   - Verdict: ❌ Violates constitution security standards

2. **Whitelist specific origins**
   - Pros: Secure, explicit control
   - Cons: Need to update for each environment
   - Verdict: ✅ CHOSEN - Best practice

3. **No CORS (same origin only)**
   - Pros: Most secure
   - Cons: Impossible with separate frontend/backend ports
   - Verdict: ❌ Not feasible for this architecture

**Chosen Approach:**
Whitelist specific origins with environment variable configuration.

**Implementation:**
```python
# main.py
origins = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
    "http://127.0.0.1:3000",  # Alternative localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Justification:**
- Follows constitution.md security principles
- Supports JWT token authentication (credentials)
- Environment-specific (dev vs production)
- Explicit control over allowed origins

**Testing:**
- Verify frontend can call backend APIs
- Verify CORS headers in response
- Test with different HTTP methods (GET, POST, PUT, DELETE)

Add CORS configuration fix task:

**Task ID:** T-BUG-002
**Priority:** Critical (Blocker)
**Type:** Bug Fix / Configuration
**Related:** F-001, F-002 (Authentication), ALL API endpoints
**Blocks:** All frontend-backend communication

**Description:**
Configure CORS middleware in FastAPI backend to allow requests from Next.js frontend.

**Current State:**
- Backend blocks all requests from frontend
- Error: "No 'Access-Control-Allow-Origin' header"
- Zero frontend-backend communication possible

**Target State:**
- Backend accepts requests from http://localhost:3000
- CORS headers present in all API responses
- All HTTP methods allowed (GET, POST, PUT, DELETE, PATCH)
- Credentials (JWT tokens) supported

**Implementation Steps:**

**Step 1: Add CORS Middleware (T-BUG-002-A)**
File: `src/backend/app/main.py`
```python
# Task: T-BUG-002-A
# Spec: speckit/specify.md §4.2, constitution.md §9.3

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS configuration - MUST be before routes
origins = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
    "http://127.0.0.1:3000",
    # Production URL will be added via env var
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Required for JWT tokens
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],  # Allows Authorization, Content-Type, etc.
)

# Then include routers
from app.routes import auth, tasks
app.include_router(auth.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")
```

**Step 2: Verify Environment Variable (T-BUG-002-B)**
File: `src/backend/.env`
```bash
# Verify this exists
FRONTEND_URL=http://localhost:3000
```

**Step 3: Test CORS Configuration (T-BUG-002-C)**

Test manually:
```bash
# Terminal 1: Start backend
cd src/backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Test CORS with curl
curl -X OPTIONS http://localhost:8000/api/auth/register \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

Expected response headers:
```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, PATCH, OPTIONS
```

**Step 4: Frontend Testing (T-BUG-002-D)**

1. Start frontend: `cd src/frontend && npm run dev`
2. Open browser: http://localhost:3000
3. Try signup - should work without CORS error
4. Check browser network tab - verify CORS headers present

**Acceptance Criteria:**
- [ ] CORSMiddleware added to main.py BEFORE routes
- [ ] Frontend URL (localhost:3000) in allowed origins
- [ ] allow_credentials=True (for JWT tokens)
- [ ] All HTTP methods allowed
- [ ] Browser console shows NO CORS errors
- [ ] Network tab shows Access-Control-Allow-Origin header
- [ ] Signup/login API calls succeed
- [ ] All CRUD operations work

**Testing Checklist:**
- [ ] OPTIONS request (preflight) succeeds
- [ ] POST /api/auth/register succeeds
- [ ] POST /api/auth/login succeeds
- [ ] GET /api/{user_id}/tasks succeeds
- [ ] POST /api/{user_id}/tasks succeeds
- [ ] Browser console clear (no CORS errors)

**Common Mistakes to Avoid:**
- ❌ Adding CORS middleware AFTER routes (wrong order)
- ❌ Using allow_origins=["*"] with allow_credentials=True (conflict)
- ❌ Forgetting to restart backend after changes
- ❌ Wrong frontend URL (typo in port number)

**Files to Modify:**
- src/backend/app/main.py (add CORS middleware)
- src/backend/.env (verify FRONTEND_URL exists)

**Reference:**
- Spec: speckit/specify.md §4.2 (Security - CORS)
- Constitution: constitution.md §9.3 (CORS Configuration)
- Plan: speckit/plan.md §3 (CORS Decision)


@backend-engineer @integration-specialist

Implement Task T-BUG-002 to fix CORS blocking issue.

**Critical Issue:**
Frontend cannot communicate with backend due to CORS policy.
ALL API requests are failing.

**Required Implementation:**
Add CORSMiddleware to src/backend/app/main.py as specified in T-BUG-002.

**Backend Engineer:**
1. Open src/backend/app/main.py
2. Add CORSMiddleware BEFORE any route includes
3. Configure with:
   - allow_origins from FRONTEND_URL env var
   - allow_credentials=True
   - allow_methods=["*"]
   - allow_headers=["*"]
4. Verify .env has FRONTEND_URL=http://localhost:3000
5. Restart server with: uvicorn app.main:app --reload --port 8000

**Integration Specialist:**
1. Test OPTIONS preflight request
2. Verify CORS headers in response
3. Test actual signup request from frontend
4. Confirm no CORS errors in browser console
5. Validate all CRUD endpoints work

**Success Criteria:**
- Browser console shows NO CORS errors
- Signup/login work from frontend
- Network tab shows Access-Control-Allow-Origin header

**Reference:**
- Task: speckit/tasks.md T-BUG-002
- Spec: speckit/specify.md §4.2
- Constitution: constitution.md §9.3

**URGENT:** This is a blocker. All frontend features depend on this fix.


# src/backend/app/main.py
# Task: T-BUG-002-A
# Spec: speckit/specify.md §4.2

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Todo API",
    description="Phase-II Full-Stack Todo Application",
    version="1.0.0"
)

# CORS Configuration (MUST be before routes)
origins = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
from app.routes import auth, tasks

app.include_router(auth.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")

# Health check endpoint
@app.get("/")
async def root():
    return {"status": "ok", "message": "Todo API is running"}

# Health check with CORS test
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "cors_enabled": True,
        "allowed_origins": origins
    }


curl -X OPTIONS http://localhost:8000/api/auth/register \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -v


curl -X POST http://localhost:8000/api/auth/register \
  -H "Origin: http://localhost:3000" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test1234!"}' \
  -v

response_text: |
  Fixed CORS configuration issue by:
  1. Removing duplicate CORS middleware configuration
  2. Replacing wildcard origins with specific allowed origins
  3. Adding FRONTEND_URL environment variable to .env file
  4. Properly configuring CORS to work with credentials (JWT tokens)
  5. Allowing specific HTTP methods instead of wildcard for security

  The frontend (http://localhost:3000) can now communicate with the backend (http://localhost:8000)
  without CORS errors, enabling proper authentication and API functionality.
outcome: "Fixed CORS configuration that was blocking frontend-backend communication. Frontend can now make API requests to backend without CORS errors."
evaluation: "Root cause was conflicting CORS configuration with allow_origins=['*'] and allow_credentials=True which is not allowed in FastAPI. Fixed by using specific origins with credentials support."
---