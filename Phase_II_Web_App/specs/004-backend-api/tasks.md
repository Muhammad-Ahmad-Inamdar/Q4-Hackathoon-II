# Tasks: Backend API Endpoints

**Input**: Design documents from `/specs/004-backend-api/`
**Prerequisites**: spec.md, plan.md, database schema (003-database-schema)
**Feature**: 004-backend-api
**Date**: 2026-02-01

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to

---

## Phase 1: Setup

**Purpose**: Create module structure and CRUD foundation

- [x] T001 Create tasks/ directory in src/backend/app/
- [x] T002 Create tasks/crud.py with database operation functions
- [x] T003 Create tasks/router.py with FastAPI router initialization

---

## Phase 2: CRUD Operations (Database Layer)

**Goal**: Implement database operations for all task CRUD

### Implementation

- [x] T004 [P] [US1] Implement create_task() in tasks/crud.py
- [x] T005 [P] [US2] Implement get_tasks_by_user() in tasks/crud.py with skip/limit
- [x] T006 [P] [US5] Implement get_task_by_id() in tasks/crud.py with user_id filter
- [x] T007 [P] [US3] Implement update_task() in tasks/crud.py with user_id filter
- [x] T008 [P] [US4] Implement delete_task() in tasks/crud.py with user_id filter

**Checkpoint**: All CRUD operations implemented with user isolation

---

## Phase 3: User Story 1 - Create Task API

**Goal**: POST /api/tasks endpoint

### Implementation

- [x] T009 [US1] Implement POST / endpoint in tasks/router.py
- [x] T010 [US1] Add JWTBearer dependency to create endpoint
- [x] T011 [US1] Extract user_id from request.state and pass to create_task()
- [x] T012 [US1] Return TaskResponse with 201 status code
- [x] T013 [US1] Add error handling for authentication and validation errors

**Checkpoint**: Create task endpoint functional with authentication

---

## Phase 4: User Story 2 - List Tasks API

**Goal**: GET /api/tasks endpoint

### Implementation

- [x] T014 [US2] Implement GET / endpoint in tasks/router.py
- [x] T015 [US2] Add skip and limit query parameters
- [x] T016 [US2] Add JWTBearer dependency and extract user_id
- [x] T017 [US2] Return List[TaskResponse] with user's tasks only

**Checkpoint**: List tasks endpoint functional with user isolation

---

## Phase 5: User Story 3 - Update Task API

**Goal**: PUT /api/tasks/{task_id} endpoint

### Implementation

- [x] T018 [US3] Implement PUT /{task_id} endpoint in tasks/router.py
- [x] T019 [US3] Add JWTBearer dependency and extract user_id
- [x] T020 [US3] Call update_task() with user_id filter
- [x] T021 [US3] Return 404 if task not found or doesn't belong to user
- [x] T022 [US3] Return updated TaskResponse

**Checkpoint**: Update task endpoint functional with user isolation

---

## Phase 6: User Story 4 - Delete Task API

**Goal**: DELETE /api/tasks/{task_id} endpoint

### Implementation

- [x] T023 [US4] Implement DELETE /{task_id} endpoint in tasks/router.py
- [x] T024 [US4] Add JWTBearer dependency and extract user_id
- [x] T025 [US4] Call delete_task() with user_id filter
- [x] T026 [US4] Return 404 if task not found or doesn't belong to user
- [x] T027 [US4] Return success message

**Checkpoint**: Delete task endpoint functional with user isolation

---

## Phase 7: User Story 5 - Get Single Task API

**Goal**: GET /api/tasks/{task_id} endpoint

### Implementation

- [x] T028 [US5] Implement GET /{task_id} endpoint in tasks/router.py
- [x] T029 [US5] Add JWTBearer dependency and extract user_id
- [x] T030 [US5] Call get_task_by_id() with user_id filter
- [x] T031 [US5] Return 404 if task not found or doesn't belong to user

**Checkpoint**: Get single task endpoint functional

---

## Phase 8: Integration

**Purpose**: Register router in main application

- [x] T032 Import tasks_router in src/backend/app/main.py
- [x] T033 Register router with app.include_router(tasks_router, prefix="/api/tasks", tags=["tasks"])
- [x] T034 Test all endpoints with curl/Postman
- [x] T035 Verify user isolation with multi-user testing
- [x] T036 Verify error responses (401, 404, 422)

**Checkpoint**: All API endpoints integrated and tested

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **CRUD Operations (Phase 2)**: Depends on Setup, requires database schema (003)
- **API Endpoints (Phase 3-7)**: All depend on Phase 2 completion
- **Integration (Phase 8)**: Depends on all endpoint phases

### Parallel Opportunities

- T004-T008 (all CRUD functions) can run in parallel
- Phase 3-7 (all API endpoints) can run in parallel after Phase 2

---

## Implementation Strategy

### Sequential Approach

1. Complete Phase 1-2: Setup and CRUD layer
2. Complete Phase 3-7: All API endpoints (can be parallel)
3. Complete Phase 8: Integration and testing

---

## Notes

- All endpoints require JWT authentication via JWTBearer middleware
- User isolation enforced by passing user_id to all CRUD operations
- 404 returned instead of 403 to avoid information leakage
- TaskCreate, TaskUpdate, TaskResponse models already defined in models.py
- Database session injected via Depends(get_session)
