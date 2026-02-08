---
description: "Task list for Phase I Todo Console App Extensions implementation"
---

# Tasks: Phase I Todo Console App Extensions

**Input**: Design documents from `/specs/001-todo-cli-extensions/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 [P] Create directory structure: src/utils/ for color utilities
- [X] T002 [P] Create tests directory structure: tests/unit/, tests/integration/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 Update Task model to include deadline field in src/todo/models.py
- [X] T004 [P] Create color utilities for CLI visual theme in src/utils/colors.py
- [X] T005 [P] Create task service with sorting and filtering logic in src/todo/services.py
- [X] T006 Update existing CLI command structure to support new options in src/cli/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - CLI Visual Enhancement (Priority: P1) 🎯 MVP

**Goal**: Apply consistent ANSI color theme to CLI output to improve readability without changing functional behavior

**Independent Test**: Can be fully tested by running the application and verifying that all displayed text uses consistent color themes that improve readability while all functional behavior remains unchanged.

### Implementation for User Story 1

- [X] T007 [P] [US1] Create ANSI color constants and helper functions in src/utils/colors.py
- [X] T008 [US1] Update CLI output functions to use color utilities in src/cli/main.py
- [X] T009 [US1] Apply color theme to task list display in src/cli/main.py
- [X] T010 [US1] Apply color theme to task creation and status messages in src/cli/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Status Toggle (Priority: P1)

**Goal**: Allow users to toggle task status both ways (Not Done ↔ Done) using task IDs with immediate visibility in task list

**Independent Test**: Can be fully tested by creating a task, toggling its status from Not Done to Done, verifying it appears as completed in the list, then toggling back to Not Done and verifying the change is reflected.

### Implementation for User Story 2

- [X] T011 [P] [US2] Create toggleStatus function in src/todo/services.py
- [X] T012 [US2] Update task model to support status toggling in src/todo/models.py
- [X] T013 [US2] Create CLI command for toggling task status in src/cli/main.py
- [X] T014 [US2] Update task list display to reflect immediate status changes in src/cli/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Creation Date Tracking (Priority: P1)

**Goal**: Each task stores a human-readable creation timestamp that is automatically assigned when created and displayed when listing tasks

**Independent Test**: Can be fully tested by creating tasks and verifying that each task displays a human-readable creation date/time that was automatically assigned at creation time.

### Implementation for User Story 3

- [X] T015 [P] [US3] Update task creation function to include timestamp in src/todo/services.py
- [X] T016 [US3] Format creation date for human-readable display in src/utils/dateFormatter.py
- [X] T017 [US3] Update task list display to show creation date in src/cli/main.py
- [X] T018 [US3] Ensure creation timestamp is preserved in JSON storage in src/todo/repository.py

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Optional Task Deadline (Priority: P2)

**Goal**: Users can optionally add a deadline date to tasks so that they can track when tasks need to be completed, with the deadline displayed if present

**Independent Test**: Can be fully tested by creating tasks with and without deadlines and verifying that deadlines are displayed when present but not shown when absent.

### Implementation for User Story 4

- [X] T019 [P] [US4] Update task model to support optional deadline field in src/todo/models.py
- [X] T020 [US4] Create deadline validation function in src/todo/services.py
- [X] T021 [US4] Update CLI add command to accept optional deadline parameter in src/cli/main.py
- [X] T022 [US4] Update task list display to show deadline when present in src/cli/main.py

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Task Sorting (Priority: P2)

**Goal**: Users can sort the task list by creation date, deadline, and completion status via CLI options

**Independent Test**: Can be fully tested by creating multiple tasks with different creation dates, deadlines, and statuses, then applying sorting options and verifying the list is correctly ordered.

### Implementation for User Story 5

- [X] T023 [P] [US5] Create sorting functions by date, deadline, and status in src/todo/services.py
- [X] T024 [US5] Add sorting CLI options (--sort-by, --order) to list command in src/cli/main.py
- [X] T025 [US5] Implement sorting logic for tasks without deadlines in src/todo/services.py
- [X] T026 [US5] Update task list display to show sorted results in src/cli/main.py

**Checkpoint**: At this point, User Stories 1, 2, 3, 4 AND 5 should all work independently

---

## Phase 8: User Story 6 - Task Filtering (Priority: P2)

**Goal**: Users can filter tasks by completion status (done/not done) so that they can focus on specific subsets of tasks without modifying underlying data

**Independent Test**: Can be fully tested by creating tasks with different completion statuses, applying filters, and verifying that only matching tasks are displayed while the underlying data remains unchanged.

### Implementation for User Story 6

- [X] T027 [P] [US6] Create filtering functions by status in src/todo/services.py
- [X] T028 [US6] Add filtering CLI options (--done, --not-done) to list command in src/cli/main.py
- [X] T029 [US6] Implement filter logic that doesn't modify original data in src/todo/services.py
- [X] T030 [US6] Update task list display to show filtered results in src/cli/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T031 [P] Update documentation to reflect new CLI options and usage in README.md
- [X] T032 Integration testing of all new features together
- [X] T033 [P] Error handling for edge cases (invalid task IDs, invalid dates, etc.) in src/cli/main.py
- [X] T034 [P] Performance optimization for large task lists
- [X] T035 Run quickstart.md validation to ensure all features work as expected

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
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 6 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all parallel tasks for User Story 1 together:
Task: "Create ANSI color constants and helper functions in src/utils/colors.js"
Task: "Update CLI output functions to use color utilities in src/cli/commands.js"
```

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 3 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (CLI Visual Enhancement)
4. Complete Phase 4: User Story 2 (Task Status Toggle)
5. Complete Phase 5: User Story 3 (Creation Date Tracking)
6. **STOP and VALIDATE**: Test User Stories 1-3 independently
7. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Stories 1-3 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 4 → Test independently → Deploy/Demo
4. Add User Story 5 → Test independently → Deploy/Demo
5. Add User Story 6 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (CLI Visual Enhancement)
   - Developer B: User Story 2 (Task Status Toggle)
   - Developer C: User Story 3 (Creation Date Tracking)
   - Developer D: User Story 4 (Optional Deadline)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence