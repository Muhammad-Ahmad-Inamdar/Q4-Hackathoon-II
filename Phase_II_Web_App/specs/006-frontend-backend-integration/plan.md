# Implementation Plan: Frontend-Backend Integration

**Branch**: `006-frontend-backend-integration` | **Date**: 2026-02-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/006-frontend-backend-integration/spec.md`

## Summary

Integrate Next.js frontend with FastAPI backend by configuring CORS, implementing centralized API client, and ensuring end-to-end authentication and CRUD operations work seamlessly. Handle errors gracefully and provide user feedback.

## Technical Context

**Language/Version**: TypeScript (frontend), Python 3.13+ (backend)
**Primary Dependencies**: Next.js 16+, FastAPI, fetch API
**Storage**: JWT tokens in memory/cookies
**Testing**: Manual end-to-end testing
**Target Platform**: Web browsers (Chrome, Firefox, Safari)
**Project Type**: Full-stack web application
**Performance Goals**: < 2s page load, < 500ms API response
**Constraints**: CORS must be configured, tokens must be secure
**Scale/Scope**: Support 1000+ concurrent users

## Constitution Check

✅ **PASS**: Spec-Driven Development followed
✅ **PASS**: Next.js App Router used
✅ **PASS**: TypeScript for frontend
✅ **PASS**: Centralized API client
✅ **PASS**: JWT authentication flow

## Project Structure

### Documentation (this feature)

```text
specs/006-frontend-backend-integration/
├── spec.md              # Feature specification
├── plan.md              # This file
└── tasks.md             # Task breakdown
```

### Source Code

```text
src/backend/app/
└── main.py              # CORS configuration

src/frontend/
├── lib/
│   ├── api.ts           # Centralized API client
│   └── auth.ts          # Auth helper functions
├── components/
│   └── auth/            # Login/Signup forms
└── app/
    ├── dashboard/       # Protected routes
    └── (auth)/          # Auth routes
```

**Structure Decision**: Backend CORS in main.py, frontend API client in lib/api.ts. Separation of concerns with auth helpers and API client.

## CORS Configuration Strategy

**Backend (FastAPI)**:
```python
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",  # Alternative port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)
```

**Key Points**:
- CORS middleware added BEFORE other middleware
- allow_credentials=True for Authorization headers
- Explicit origins (not wildcard in production)
- All HTTP methods allowed

## API Client Architecture

**Frontend (lib/api.ts)**:
```typescript
class ApiClient {
  private baseURL: string;
  private getToken(): string | null;

  async request(endpoint, options) {
    // Add Authorization header if token exists
    // Handle errors (401 -> redirect to login)
    // Parse JSON response
    // Throw on error status
  }

  // Convenience methods
  get(endpoint)
  post(endpoint, data)
  put(endpoint, data)
  delete(endpoint)
}
```

**Features**:
- Automatic token injection
- Centralized error handling
- Type-safe with TypeScript
- Environment-based API URL

## Authentication Flow

### Registration Flow
1. User fills signup form
2. Frontend calls `api.post('/api/auth/register', { email, password })`
3. Backend creates user and returns token
4. Frontend stores token (memory/cookie)
5. Frontend redirects to dashboard

### Login Flow
1. User fills login form
2. Frontend calls `api.post('/api/auth/login', { email, password })`
3. Backend validates credentials and returns token
4. Frontend stores token
5. Frontend redirects to dashboard

### Protected Route Access
1. User navigates to /dashboard
2. Frontend checks for token
3. If no token, redirect to /login
4. If token exists, fetch tasks with `api.get('/api/tasks')`
5. Display tasks in UI

## Error Handling Strategy

**Network Errors**:
- Catch fetch errors
- Display "Network error, please try again"
- Don't crash the app

**401 Unauthorized**:
- Clear stored token
- Redirect to /login
- Show "Session expired, please login again"

**422 Validation Error**:
- Parse error details from response
- Display field-specific errors
- Highlight invalid fields

**500 Server Error**:
- Display "Server error, please try again later"
- Log error for debugging
- Don't expose technical details to user

## Environment Configuration

**Backend (.env)**:
```
FRONTEND_URL=http://localhost:3000
```

**Frontend (.env.local)**:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Integration Testing Checklist

- [ ] Frontend can reach backend health endpoint
- [ ] CORS allows requests from frontend origin
- [ ] Registration creates user and returns token
- [ ] Login validates credentials and returns token
- [ ] Protected routes redirect unauthenticated users
- [ ] Task creation persists to backend
- [ ] Task list fetches from backend
- [ ] Task update saves to backend
- [ ] Task delete removes from backend
- [ ] 401 errors trigger re-authentication
- [ ] Network errors show user-friendly messages

## Security Considerations

- Tokens stored securely (not localStorage for production)
- HTTPS in production (not HTTP)
- CORS origins restricted to known domains
- No sensitive data in error messages
- Token expiration handled gracefully

## Acceptance Criteria

- [ ] CORS configured to allow frontend requests
- [ ] API client implemented with automatic token injection
- [ ] Authentication flow works end-to-end
- [ ] Task CRUD operations work through frontend
- [ ] Error handling displays appropriate messages
- [ ] Loading states shown during API requests
- [ ] Token expiration triggers re-authentication
