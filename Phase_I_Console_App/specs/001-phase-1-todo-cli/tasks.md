---
description: "Task list for Phase I Todo CLI application implementation"
---

# Tasks: Phase I - In-Memory Python Console Todo App

**Input**: Design documents from `/specs/001-phase-1-todo-cli/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Python CLI app**: `src/todo/` for domain logic, `src/cli/` for interface
- Paths shown below follow the plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in src/
- [x] T002 Create src/todo/ directory structure
- [x] T003 Create src/cli/ directory structure
- [x] T004 Create __init__.py files in src/todo/ and src/cli/ directories

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 [P] Create Todo model in src/todo/models.py with id, title, description, completed attributes
- [x] T006 [P] Create in-memory repository in src/todo/repository.py with add, get_by_id, get_all, update, delete methods
- [x] T007 [P] Create TodoService in src/todo/services.py with add_task, get_all_tasks, get_task_by_id, update_task, complete_task, delete_task methods
- [x] T008 Create deterministic ID generation in repository layer

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks and view all tasks with their status

**Independent Test**: User can add a task with a title and see it appear in the task list with a unique ID and "incomplete" status

### Implementation for User Story 1

- [x] T009 [P] [US1] Implement add_task functionality in src/todo/services.py
- [x] T010 [P] [US1] Implement get_all_tasks functionality in src/todo/services.py
- [x] T011 [US1] Create CLI command parser in src/cli/main.py to handle 'add' command
- [x] T012 [US1] Create CLI command parser in src/cli/main.py to handle 'list' command
- [x] T013 [US1] Implement CLI display for task list in src/cli/main.py
- [x] T014 [US1] Connect CLI add command to service layer in src/cli/main.py
- [x] T015 [US1] Connect CLI list command to service layer in src/cli/main.py
- [x] T016 [US1] Implement basic menu loop in src/cli/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Complete and Update Tasks (Priority: P2)

**Goal**: Enable users to mark tasks as complete/incomplete and update task details

**Independent Test**: User can mark a task as complete using its ID and update task details without changing completion status

### Implementation for User Story 2

- [x] T017 [P] [US2] Implement complete_task and incomplete_task methods in src/todo/services.py
- [x] T018 [P] [US2] Implement update_task functionality in src/todo/services.py preserving completion status
- [x] T019 [US2] Create CLI command parser in src/cli/main.py to handle 'complete' command
- [x] T020 [US2] Create CLI command parser in src/cli/main.py to handle 'incomplete' command
- [x] T021 [US2] Create CLI command parser in src/cli/main.py to handle 'update' command
- [x] T022 [US2] Connect CLI complete command to service layer in src/cli/main.py
- [x] T023 [US2] Connect CLI incomplete command to service layer in src/cli/main.py
- [x] T024 [US2] Connect CLI update command to service layer in src/cli/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Delete Tasks (Priority: P3)

**Goal**: Enable users to remove tasks from the system by ID

**Independent Test**: User can delete a task by ID and verify it no longer appears in the task list

### Implementation for User Story 3

- [x] T025 [US3] Create CLI command parser in src/cli/main.py to handle 'delete' command
- [x] T026 [US3] Connect CLI delete command to service layer in src/cli/main.py
- [x] T027 [US3] Test delete functionality integration with CLI and services

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T028 [P] Add error handling for invalid task IDs in src/todo/services.py
- [ ] T029 [P] Add input validation for task titles in src/todo/models.py
- [ ] T030 Add user-friendly error messages in src/cli/main.py
- [ ] T031 [P] Add docstrings and type hints to all functions and methods
- [ ] T032 Implement graceful exit functionality in src/cli/main.py
- [ ] T033 Add README documentation with usage instructions
- [x] T034 [P] Implement JSON serialization in src/todo/repository.py
- [x] T035 [P] Implement file loading on startup in src/todo/repository.py
- [x] T036 [P] Implement file saving on exit in src/todo/repository.py
- [x] T037 [P] Update CLI to handle file persistence in src/cli/main.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before CLI interface
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Implement add_task functionality in src/todo/services.py"
Task: "Implement get_all_tasks functionality in src/todo/services.py"

# Launch all CLI components for User Story 1 together:
Task: "Create CLI command parser in src/cli/main.py to handle 'add' command"
Task: "Create CLI command parser in src/cli/main.py to handle 'list' command"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence