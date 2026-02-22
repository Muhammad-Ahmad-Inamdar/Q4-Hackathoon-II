# Tasks: Authentication System

**Input**: Design documents from `/specs/005-authentication-system/`
**Prerequisites**: spec.md, plan.md, database schema (003-database-schema)
**Feature**: 005-authentication-system
**Date**: 2026-02-01

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to

---

## Phase 1: Setup

**Purpose**: Create auth module structure

- [x] T001 Create auth/ directory in src/backend/app/
- [x] T002 Create auth/service.py for business logic
- [x] T003 Create auth/router.py for API endpoints
- [x] T004 Create auth/middleware.py for JWT validation

---

## Phase 2: Authentication Service Layer

**Goal**: Implement core authentication logic

### Implementation

- [x] T005 [P] [US1] Implement create_user() in auth/service.py with bcrypt password hashing
- [x] T006 [P] [US2] Implement authenticate_user() in auth/service.py with bcrypt verification
- [x] T007 [P] [US3] Implement create_access_token() in auth/service.py with JWT generation
- [x] T008 [P] [US3] Implement verify_token() in auth/service.py with JWT validation
- [x] T009 Add BETTER_AUTH_SECRET loading from environment in service.py
- [x] T010 Set JWT expiration to 30 minutes in create_access_token()

**Checkpoint**: All authentication business logic implemented

---

## Phase 3: User Story 1 - User Registration

**Goal**: POST /api/auth/register endpoint

### Implementation

- [x] T011 [US1] Implement POST /register endpoint in auth/router.py
- [x] T012 [US1] Add email uniqueness check before user creation
- [x] T013 [US1] Call create_user() from service layer
- [x] T014 [US1] Generate JWT token after successful registration
- [x] T015 [US1] Return Token response with access_token
- [x] T016 [US1] Add error handling for duplicate email (400 Bad Request)
- [x] T017 [US1] Add error handling for database errors (500 Internal Server Error)

**Checkpoint**: User registration endpoint functional

---

## Phase 4: User Story 2 - User Login

**Goal**: POST /api/auth/login endpoint

### Implementation

- [x] T018 [US2] Implement POST /login endpoint in auth/router.py
- [x] T019 [US2] Call authenticate_user() from service layer
- [x] T020 [US2] Return 401 Unauthorized for invalid credentials
- [x] T021 [US2] Update last_login_at timestamp on successful login
- [x] T022 [US2] Generate JWT token after successful authentication
- [x] T023 [US2] Return Token response with access_token

**Checkpoint**: User login endpoint functional

---

## Phase 5: User Story 3 - Token Validation Middleware

**Goal**: JWTBearer middleware for protecting endpoints

### Implementation

- [x] T024 [US3] Create JWTBearer class extending HTTPBearer in auth/middleware.py
- [x] T025 [US3] Implement __call__ method to extract token from Authorization header
- [x] T026 [US3] Call verify_token() to validate JWT signature and expiration
- [x] T027 [US3] Extract user_id from token payload
- [x] T028 [US3] Set request.state.user_id for route handlers
- [x] T029 [US3] Raise HTTPException(401) for invalid/expired tokens
- [x] T030 [US3] Handle missing Authorization header (401 Unauthorized)

**Checkpoint**: JWT middleware functional and ready for use

---

## Phase 6: User Story 4 - User Logout

**Goal**: POST /api/auth/logout endpoint

### Implementation

- [x] T031 [US4] Implement POST /logout endpoint in auth/router.py
- [x] T032 [US4] Return success message (stateless JWT, client-side removal)

**Checkpoint**: Logout endpoint functional

---

## Phase 7: Integration

**Purpose**: Register auth router and test authentication flow

- [x] T033 Import auth_router in src/backend/app/main.py
- [x] T034 Register router with app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
- [x] T035 Set BETTER_AUTH_SECRET in main.py using os.environ.setdefault()
- [x] T036 Test registration endpoint with valid credentials
- [x] T037 Test registration endpoint with duplicate email (expect 400)
- [x] T038 Test login endpoint with valid credentials
- [x] T039 Test login endpoint with invalid credentials (expect 401)
- [x] T040 Test protected endpoint with valid JWT token (expect success)
- [x] T041 Test protected endpoint with invalid JWT token (expect 401)
- [x] T042 Test protected endpoint without Authorization header (expect 401)
- [x] T043 Verify password is hashed in database (not plain text)
- [x] T044 Verify last_login_at is updated on login

**Checkpoint**: Authentication system fully integrated and tested

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Service Layer (Phase 2)**: Depends on Setup
- **Registration (Phase 3)**: Depends on Phase 2
- **Login (Phase 4)**: Depends on Phase 2
- **Middleware (Phase 5)**: Depends on Phase 2
- **Logout (Phase 6)**: Can run parallel with Phase 3-5
- **Integration (Phase 7)**: Depends on all previous phases

### Parallel Opportunities

- T005-T010 (all service functions) can run in parallel
- Phase 3, 4, 5, 6 (all endpoints and middleware) can run in parallel after Phase 2

---

## Implementation Strategy

### Sequential Approach

1. Complete Phase 1-2: Setup and service layer
2. Complete Phase 3-6: All endpoints and middleware (can be parallel)
3. Complete Phase 7: Integration and comprehensive testing

---

## Notes

- bcrypt.hashpw() for password hashing, bcrypt.checkpw() for verification
- JWT tokens signed with HS256 algorithm
- BETTER_AUTH_SECRET must match between backend and Better Auth (if used)
- Token expiration set to 30 minutes (1800 seconds)
- User model already exists from 003-database-schema
- JWTBearer middleware will be used by task endpoints (004-backend-api)
