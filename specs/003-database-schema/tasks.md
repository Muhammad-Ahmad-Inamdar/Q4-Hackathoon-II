# Tasks: Database Schema Design

**Input**: Design documents from `/specs/003-database-schema/`
**Prerequisites**: spec.md, plan.md
**Feature**: 003-database-schema
**Date**: 2026-01-31

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2)

---

## Phase 1: Setup

**Purpose**: Database infrastructure setup

- [x] T001 Install SQLModel and PostgreSQL dependencies in requirements.txt
- [x] T002 Configure DATABASE_URL in .env file
- [x] T003 [P] Create database.py with connection logic and get_session() function

---

## Phase 2: User Story 1 - User Data Persistence

**Goal**: Create User table with authentication fields

### Implementation for User Story 1

- [x] T004 Create User model in src/backend/app/models.py with fields: id, email, password, created_at, updated_at, last_login_at
- [x] T005 Add unique constraint on User.email field
- [x] T006 Add UserRegistration and UserLogin schemas in models.py
- [x] T007 Add Token response schema in models.py

**Checkpoint**: User table schema defined and ready for creation

---

## Phase 3: User Story 2 - Task Data Persistence with User Isolation

**Goal**: Create Task table with user_id foreign key

### Implementation for User Story 2

- [x] T008 Create TaskBase model in src/backend/app/models.py with title, description, completed
- [x] T009 Create Task model extending TaskBase with id, user_id (foreign key), created_at, updated_at
- [x] T010 Add TaskCreate, TaskUpdate, TaskResponse schemas in models.py
- [x] T011 Add field validation: title (1-255 chars), description (0-1000 chars)

**Checkpoint**: Task table schema defined with user isolation

---

## Phase 4: Database Initialization

**Purpose**: Create tables in database

- [x] T012 Create create_tables() function in database.py using SQLModel.metadata.create_all()
- [x] T013 Create create_db_tables.py script for manual table creation
- [x] T014 Test database connection and table creation
- [x] T015 Verify User table exists with correct schema
- [x] T016 Verify Task table exists with user_id foreign key constraint

**Checkpoint**: Database tables created and verified

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **User Story 1 (Phase 2)**: Depends on Setup
- **User Story 2 (Phase 3)**: Depends on Setup (can run parallel with Phase 2)
- **Database Initialization (Phase 4)**: Depends on Phase 2 and Phase 3 completion

### Parallel Opportunities

- T004-T007 (User models) can run parallel with T008-T011 (Task models)
- T015-T016 (verification) can run in parallel

---

## Implementation Strategy

### Sequential Approach

1. Complete Phase 1: Setup database connection
2. Complete Phase 2 & 3: Define all models
3. Complete Phase 4: Create tables and verify

---

## Notes

- All models use SQLModel (not raw SQLAlchemy)
- UUID primary keys generated using uuid.uuid4()
- Timestamps use datetime.utcnow()
- Password hashing handled at service layer (not in models)
- Foreign key constraint enforces user isolation
