# Tasks: Frontend-Backend Integration

**Input**: Design documents from `/specs/006-frontend-backend-integration/`
**Prerequisites**: spec.md, plan.md, backend API (004), authentication (005)
**Feature**: 006-frontend-backend-integration
**Date**: 2026-02-02

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to

---

## Phase 1: User Story 1 - CORS Configuration

**Goal**: Enable cross-origin requests from frontend to backend

### Implementation

- [x] T001 [US1] Add FRONTEND_URL to backend .env file
- [x] T002 [US1] Import CORSMiddleware in src/backend/app/main.py
- [x] T003 [US1] Configure allowed origins list (localhost:3000, 127.0.0.1:3000)
- [x] T004 [US1] Add CORSMiddleware to FastAPI app with allow_credentials=True
- [x] T005 [US1] Set allow_methods to include all HTTP verbs
- [x] T006 [US1] Set allow_headers to ["*"]
- [x] T007 [US1] Ensure CORS middleware is added BEFORE other middleware
- [x] T008 [US1] Test preflight OPTIONS request from frontend
- [x] T009 [US1] Verify CORS headers in response

**Checkpoint**: CORS configured and frontend can make requests

---

## Phase 2: User Story 2 - API Client Implementation

**Goal**: Create centralized API client for frontend

### Implementation

- [x] T010 [US2] Create src/frontend/lib/api.ts file
- [x] T011 [US2] Add NEXT_PUBLIC_API_URL to frontend .env.local
- [x] T012 [US2] Implement ApiClient class with baseURL from env
- [x] T013 [US2] Implement getToken() method to retrieve stored token
- [x] T014 [US2] Implement request() method with Authorization header injection
- [x] T015 [US2] Add error handling for network errors in request()
- [x] T016 [US2] Add error handling for 401 (redirect to login)
- [x] T017 [US2] Add error handling for other HTTP errors
- [x] T018 [US2] Implement convenience methods: get(), post(), put(), delete()
- [x] T019 [US2] Export singleton instance of ApiClient
- [x] T020 [US2] Add TypeScript types for request/response

**Checkpoint**: API client ready for use in components

---

## Phase 3: User Story 3 - Authentication Flow Integration

**Goal**: Connect frontend auth forms to backend auth endpoints

### Implementation

- [x] T021 [US3] Create src/frontend/lib/auth.ts with token storage functions
- [x] T022 [US3] Implement setToken() and getToken() functions
- [x] T023 [US3] Implement clearToken() function
- [x] T024 [US3] Update SignupForm to call api.post('/api/auth/register')
- [x] T025 [US3] Store token after successful registration
- [x] T026 [US3] Redirect to dashboard after registration
- [x] T027 [US3] Update LoginForm to call api.post('/api/auth/login')
- [x] T028 [US3] Store token after successful login
- [x] T029 [US3] Redirect to dashboard after login
- [x] T030 [US3] Implement route protection in dashboard layout
- [x] T031 [US3] Check for token on dashboard access
- [x] T032 [US3] Redirect to login if no token
- [x] T033 [US3] Test registration flow end-to-end
- [x] T034 [US3] Test login flow end-to-end
- [x] T035 [US3] Test protected route access

**Checkpoint**: Authentication flow works end-to-end

---

## Phase 4: User Story 4 - Task CRUD Integration

**Goal**: Connect frontend task components to backend task endpoints

### Implementation

- [x] T036 [US4] Update task creation to call api.post('/api/tasks', taskData)
- [x] T037 [US4] Update task list to call api.get('/api/tasks')
- [x] T038 [US4] Update task update to call api.put(`/api/tasks/${id}`, updates)
- [x] T039 [US4] Update task delete to call api.delete(`/api/tasks/${id}`)
- [x] T040 [US4] Add loading states during API requests
- [x] T041 [US4] Refresh task list after create/update/delete
- [x] T042 [US4] Test create task through UI
- [x] T043 [US4] Test update task through UI
- [x] T044 [US4] Test delete task through UI
- [x] T045 [US4] Verify tasks persist across page refresh

**Checkpoint**: Task CRUD operations work through frontend

---

## Phase 5: User Story 5 - Error Handling Integration

**Goal**: Display user-friendly error messages

### Implementation

- [x] T046 [US5] Add error state to auth forms
- [x] T047 [US5] Display error messages for failed registration
- [x] T048 [US5] Display error messages for failed login
- [x] T049 [US5] Add error state to task components
- [x] T050 [US5] Display error messages for failed task operations
- [x] T051 [US5] Test network error handling (backend down)
- [x] T052 [US5] Test 401 error handling (invalid token)
- [x] T053 [US5] Test validation error handling (invalid data)
- [x] T054 [US5] Verify error messages are user-friendly

**Checkpoint**: Error handling complete with user feedback

---

## Phase 6: End-to-End Testing

**Purpose**: Comprehensive integration testing

- [x] T055 Start backend server on port 8000
- [x] T056 Start frontend server on port 3000
- [x] T057 Test health endpoint from browser
- [x] T058 Register new user through UI
- [x] T059 Verify user created in database
- [x] T060 Login with registered user
- [x] T061 Verify redirect to dashboard
- [x] T062 Create multiple tasks through UI
- [x] T063 Verify tasks appear in list
- [x] T064 Update task through UI
- [x] T065 Verify update persists
- [x] T066 Delete task through UI
- [x] T067 Verify task removed from database
- [x] T068 Test with multiple users (user isolation)
- [x] T069 Verify User A cannot see User B's tasks
- [x] T070 Test token expiration (wait 30 minutes or modify expiry)
- [x] T071 Verify redirect to login after expiration

**Checkpoint**: Full integration verified end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **CORS (Phase 1)**: No dependencies, must be done first
- **API Client (Phase 2)**: Depends on CORS being configured
- **Auth Flow (Phase 3)**: Depends on API Client
- **Task CRUD (Phase 4)**: Depends on Auth Flow
- **Error Handling (Phase 5)**: Can run parallel with Phase 3-4
- **E2E Testing (Phase 6)**: Depends on all previous phases

### Parallel Opportunities

- T010-T020 (API client implementation) can be done while testing CORS
- T046-T054 (error handling) can be done parallel with Phase 3-4

---

## Implementation Strategy

### Sequential Approach

1. Complete Phase 1: CORS configuration (backend)
2. Complete Phase 2: API client (frontend)
3. Complete Phase 3: Auth flow integration
4. Complete Phase 4: Task CRUD integration
5. Complete Phase 5: Error handling
6. Complete Phase 6: Comprehensive E2E testing

---

## Notes

- CORS must be configured before any frontend requests will work
- API client should be singleton to avoid multiple instances
- Token storage strategy: use cookies or memory (not localStorage in production)
- All API calls should go through centralized API client
- Error handling should be consistent across all components
- User isolation must be verified with multi-user testing
