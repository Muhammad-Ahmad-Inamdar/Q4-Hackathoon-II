# Implementation Plan: Backend API Endpoints

**Branch**: `004-backend-api` | **Date**: 2026-02-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-backend-api/spec.md`

## Summary

Implement RESTful API endpoints for task CRUD operations using FastAPI. Separate concerns into router layer (HTTP handling) and CRUD layer (database operations). Enforce JWT authentication and user isolation on all endpoints.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: FastAPI, SQLModel, Pydantic
**Storage**: PostgreSQL via SQLModel
**Testing**: Manual testing with curl/Postman
**Target Platform**: Linux/Windows server
**Project Type**: Web application (backend)
**Performance Goals**: < 200ms p95 latency
**Constraints**: JWT authentication required, user isolation mandatory
**Scale/Scope**: Support 1000+ concurrent requests

## Constitution Check

✅ **PASS**: Spec-Driven Development followed
✅ **PASS**: RESTful API conventions followed
✅ **PASS**: User isolation enforced via user_id filtering
✅ **PASS**: JWT authentication on all endpoints
✅ **PASS**: Separation of concerns (router + CRUD)

## Project Structure

### Documentation (this feature)

```text
specs/004-backend-api/
├── spec.md              # Feature specification
├── plan.md              # This file
└── tasks.md             # Task breakdown
```

### Source Code (repository root)

```text
src/backend/app/
├── tasks/
│   ├── router.py        # FastAPI router with endpoints
│   └── crud.py          # Database CRUD operations
├── auth/
│   └── middleware.py    # JWT authentication middleware
├── models.py            # Task models (already exists)
├── database.py          # Database session (already exists)
└── main.py              # FastAPI app with router registration
```

**Structure Decision**: Separate tasks module with router and CRUD. Router handles HTTP concerns, CRUD handles database operations. Middleware validates JWT tokens.

## API Endpoints Design

### POST /api/tasks
- **Purpose**: Create new task
- **Auth**: Required (JWT Bearer token)
- **Request Body**: `TaskCreate` (title, description, completed)
- **Response**: `TaskResponse` (201 Created)
- **Errors**: 401 Unauthorized, 422 Validation Error

### GET /api/tasks
- **Purpose**: List all user's tasks
- **Auth**: Required (JWT Bearer token)
- **Query Params**: skip (default 0), limit (default 100)
- **Response**: `List[TaskResponse]` (200 OK)
- **Errors**: 401 Unauthorized

### GET /api/tasks/{task_id}
- **Purpose**: Get single task by ID
- **Auth**: Required (JWT Bearer token)
- **Path Param**: task_id (UUID string)
- **Response**: `TaskResponse` (200 OK)
- **Errors**: 401 Unauthorized, 404 Not Found

### PUT /api/tasks/{task_id}
- **Purpose**: Update existing task
- **Auth**: Required (JWT Bearer token)
- **Path Param**: task_id (UUID string)
- **Request Body**: `TaskUpdate` (partial update)
- **Response**: `TaskResponse` (200 OK)
- **Errors**: 401 Unauthorized, 404 Not Found, 422 Validation Error

### DELETE /api/tasks/{task_id}
- **Purpose**: Delete task
- **Auth**: Required (JWT Bearer token)
- **Path Param**: task_id (UUID string)
- **Response**: `{"message": "Task deleted successfully"}` (200 OK)
- **Errors**: 401 Unauthorized, 404 Not Found

## Authentication Flow

1. Client sends request with `Authorization: Bearer <token>` header
2. JWTBearer middleware validates token
3. Middleware extracts user_id from token payload
4. Middleware sets `request.state.user_id` for route handlers
5. Route handler retrieves user_id from request.state
6. CRUD operations filter by user_id

## User Isolation Strategy

**Database Level**: All CRUD queries include `WHERE user_id = ?` filter

**API Level**:
- Extract user_id from JWT token (not from request body)
- Pass user_id to all CRUD operations
- Return 404 if task doesn't belong to user (not 403 to avoid info leakage)

## Error Handling

**401 Unauthorized**: Invalid/missing JWT token
**404 Not Found**: Task doesn't exist or doesn't belong to user
**422 Validation Error**: Invalid request payload
**500 Internal Server Error**: Database or server errors

## CRUD Operations

```python
# crud.py functions
create_task(session, task: Task) -> Task
get_tasks_by_user(session, user_id, skip, limit) -> List[Task]
get_task_by_id(session, task_id, user_id) -> Optional[Task]
update_task(session, task_id, user_id, updates) -> Optional[Task]
delete_task(session, task_id, user_id) -> bool
```

## Dependency Injection

- `session: Session = Depends(get_session)` - Database session
- `token: str = Depends(JWTBearer())` - JWT validation
- `request: Request` - Access to request.state.user_id

## Acceptance Criteria

- [ ] All 5 CRUD endpoints implemented and functional
- [ ] JWT authentication enforced on all endpoints
- [ ] User isolation verified (multi-user testing)
- [ ] Appropriate HTTP status codes returned
- [ ] Request validation using Pydantic models
- [ ] Error handling for all edge cases
- [ ] Router registered in main.py with /api/tasks prefix
