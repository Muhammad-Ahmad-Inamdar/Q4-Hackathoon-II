# Tasks: Phase-III Todo AI Chatbot Integration

**Input**: Design documents from `/specs/007-ai-chatbot-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `src/backend/`, `src/frontend/`
- Paths follow the existing project structure (integrate into src/ directory)
- Backend: Add new directories alongside existing app/ directory
- Frontend: Add chat/ components and extend existing lib/api.ts

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and environment configuration

- [ ] T001 Configure environment variables for backend in src/backend/.env (DATABASE_URL, COHERE_API_KEY, JWT_SECRET, BETTER_AUTH_SECRET)
- [ ] T002 Configure environment variables for frontend in src/frontend/.env.local (NEXT_PUBLIC_API_URL)
- [ ] T003 [P] Install backend dependencies in src/backend/ (cohere>=4.0.0, python-jose[cryptography]>=3.3.0, pydantic>=2.0.0)
- [ ] T004 [P] Install frontend dependencies in src/frontend/ (already installed - verify versions)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Execute database migration 007_add_conversation_tables.sql to create conversations and messages tables
- [ ] T006 [P] Create Conversation model in src/backend/models/conversation.py with SQLModel
- [ ] T007 [P] Create Message model in src/backend/models/message.py with SQLModel
- [ ] T008 Implement ConversationService in src/backend/services/conversation_service.py for CRUD operations
- [ ] T009 [P] Create MCP server setup in src/backend/mcp/server.py using Official MCP SDK
- [ ] T010 [P] Implement add_task MCP tool in src/backend/mcp/tools.py with schema validation (reuses existing app/tasks/crud.py)
- [ ] T011 [P] Implement list_tasks MCP tool in src/backend/mcp/tools.py with filter parameter (reuses existing app/tasks/crud.py)
- [ ] T012 [P] Implement update_task MCP tool in src/backend/mcp/tools.py with user_id validation (reuses existing app/tasks/crud.py)
- [ ] T013 [P] Implement complete_task MCP tool in src/backend/mcp/tools.py with idempotency (reuses existing app/tasks/crud.py)
- [ ] T014 [P] Implement delete_task MCP tool in src/backend/mcp/tools.py with ownership check (reuses existing app/tasks/crud.py)
- [ ] T015 Create Cohere adapter in src/backend/agents/cohere_adapter.py to integrate Cohere API with OpenAI Agents SDK
- [ ] T016 Implement JWT validation helper in src/backend/api/auth.py (reuses existing app/auth/middleware.py JWTBearer)
- [ ] T017 [P] Setup logging infrastructure in src/backend/utils/logger.py for tool call logging
- [ ] T018 [P] Create chat service in src/backend/services/chat_service.py for stateless request processing

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 & 2 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to create and view tasks through natural language in chatbot pop-up

**Independent Test**: Open chatbot from Dashboard, type "Add buy groceries", verify task created. Then type "Show my tasks", verify task list displayed.

### Implementation for User Story 1 & 2

- [ ] T019 [US1] [US2] Implement TodoAgent in src/backend/agents/todo_agent.py with Cohere API and MCP tool orchestration
- [ ] T020 [US1] [US2] Add intent detection logic in TodoAgent to map natural language to add_task and list_tasks tools
- [ ] T021 [US1] [US2] Add tool selection logic in TodoAgent using tool-reasoning skill
- [ ] T022 [US1] [US2] Add response generation logic in TodoAgent using response-confirmation skill
- [ ] T023 [US1] [US2] Implement error recovery in TodoAgent using error-recovery skill for tool failures
- [ ] T024 [US1] [US2] Create POST /api/{user_id}/chat endpoint in src/backend/api/chat.py
- [ ] T025 [US1] [US2] Add JWT validation to chat endpoint using auth middleware (reuse existing app/auth/middleware.py)
- [ ] T026 [US1] [US2] Implement conversation history fetching in chat endpoint (stateless-context-rebuild)
- [ ] T027 [US1] [US2] Implement AI agent invocation in chat endpoint with reconstructed context
- [ ] T028 [US1] [US2] Implement message persistence in chat endpoint after agent response
- [ ] T029 [US1] [US2] Add error handling and logging to chat endpoint
- [ ] T030 [P] [US1] [US2] Create ChatbotPopup component in src/frontend/components/chat/ChatbotPopup.tsx with open/close state
- [ ] T031 [P] [US1] [US2] Create ChatMessage component in src/frontend/components/chat/ChatMessage.tsx for displaying messages
- [ ] T032 [P] [US1] [US2] Create ChatInput component in src/frontend/components/chat/ChatInput.tsx with send functionality
- [ ] T033 [US1] [US2] Extend existing src/frontend/lib/api.ts to add chat API functions (sendMessage, getConversationHistory)
- [ ] T034 [US1] [US2] Create useChat hook in src/frontend/hooks/useChat.ts for chat state management
- [ ] T035 [US1] [US2] Add ChatbotPopup to Dashboard page in src/frontend/app/dashboard/page.tsx
- [ ] T036 [US1] [US2] Add ChatbotPopup to Home page in src/frontend/app/page.tsx
- [ ] T037 [US1] [US2] Style ChatbotPopup with TailwindCSS for responsive design (mobile, tablet, desktop)
- [ ] T038 [US1] [US2] Add floating action button for chatbot with z-index positioning
- [ ] T039 [US1] [US2] Implement loading states in chatbot UI during API calls
- [ ] T040 [US1] [US2] Implement error message display in chatbot UI

**Checkpoint**: At this point, users can create and view tasks through chatbot. This is the MVP.

---

## Phase 4: User Story 3 - Complete Tasks (Priority: P2)

**Goal**: Enable users to mark tasks as complete through natural language

**Independent Test**: Create a task via chatbot, then say "Mark buy groceries as complete", verify task status changes to completed.

### Implementation for User Story 3

- [ ] T041 [US3] Add complete task intent detection to TodoAgent in src/backend/agents/todo_agent.py
- [ ] T042 [US3] Add complete_task tool selection logic to TodoAgent
- [ ] T043 [US3] Add completion confirmation response generation to TodoAgent
- [ ] T044 [US3] Handle "task already completed" scenario in TodoAgent with friendly message
- [ ] T045 [US3] Handle "task not found" error in TodoAgent with helpful suggestion

**Checkpoint**: Users can now complete tasks conversationally

---

## Phase 5: User Story 4 - Update Tasks (Priority: P2)

**Goal**: Enable users to modify task titles through natural language

**Independent Test**: Create a task, then say "Change buy milk to buy milk and eggs", verify task title updated.

### Implementation for User Story 4

- [ ] T046 [US4] Add update task intent detection to TodoAgent in src/backend/agents/todo_agent.py
- [ ] T047 [US4] Add update_task tool selection logic to TodoAgent
- [ ] T048 [US4] Add update confirmation response generation to TodoAgent
- [ ] T049 [US4] Handle ambiguous update requests in TodoAgent with clarifying questions
- [ ] T050 [US4] Handle "task not found" error for updates in TodoAgent

**Checkpoint**: Users can now update tasks conversationally

---

## Phase 6: User Story 5 - Delete Tasks (Priority: P3)

**Goal**: Enable users to delete tasks through natural language

**Independent Test**: Create a task, then say "Delete the meeting task", verify task removed from list.

### Implementation for User Story 5

- [ ] T051 [US5] Add delete task intent detection to TodoAgent in src/backend/agents/todo_agent.py
- [ ] T052 [US5] Add delete_task tool selection logic to TodoAgent
- [ ] T053 [US5] Add deletion confirmation response generation to TodoAgent
- [ ] T054 [US5] Handle multiple matching tasks in TodoAgent by listing options and asking for clarification
- [ ] T055 [US5] Handle "task not found" error for deletions in TodoAgent

**Checkpoint**: Users can now delete tasks conversationally

---

## Phase 7: User Story 6 - Conversation History (Priority: P3)

**Goal**: Maintain conversation history across sessions for contextual interactions

**Independent Test**: Have a conversation, close chatbot, reopen it, verify previous messages displayed.

### Implementation for User Story 6

- [ ] T056 [US6] Implement conversation history loading in ChatbotPopup component on mount
- [ ] T057 [US6] Display previous messages in chronological order in chatbot UI
- [ ] T058 [US6] Implement context-aware responses in TodoAgent (e.g., "Mark the first one as complete")
- [ ] T059 [US6] Add conversation_id persistence in frontend chat state
- [ ] T060 [US6] Implement context window truncation in chat endpoint for conversations exceeding 1000 messages
- [ ] T061 [US6] Add greeting message for new users with no conversation history

**Checkpoint**: Conversation history is now fully functional across sessions

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T062 [P] Add comprehensive error logging for all MCP tool calls in src/backend/mcp/tools.py
- [ ] T063 [P] Add performance monitoring for chat endpoint response times
- [ ] T064 [P] Optimize database queries with EXPLAIN ANALYZE for conversation history fetching
- [ ] T065 [P] Add rate limiting to chat endpoint to prevent abuse
- [ ] T066 [P] Implement input sanitization for all user messages to prevent injection attacks
- [ ] T067 [P] Add user-friendly error messages for Cohere API failures
- [ ] T068 [P] Test chatbot pop-up responsiveness on mobile devices
- [ ] T069 [P] Test chatbot pop-up z-index conflicts with existing UI components
- [ ] T070 [P] Validate all MCP tool schemas match contracts in contracts/mcp-tools.yaml
- [ ] T071 [P] Add documentation comments to all backend services and agents
- [ ] T072 [P] Add TypeScript types for all frontend components and services
- [ ] T073 Run manual end-to-end testing for all 6 user stories
- [ ] T074 Verify constitution compliance (statelessness, safety, observability)
- [ ] T075 Update quickstart.md with any deployment notes or troubleshooting tips

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User Stories 1 & 2 (Phase 3): Can start after Foundational - MVP
  - User Story 3 (Phase 4): Can start after Foundational - Independent of US1/US2
  - User Story 4 (Phase 5): Can start after Foundational - Independent of US1/US2/US3
  - User Story 5 (Phase 6): Can start after Foundational - Independent of other stories
  - User Story 6 (Phase 7): Can start after Foundational - Independent of other stories
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Stories 1 & 2 (P1)**: Combined into single phase as they form the MVP together (create + view)
- **User Story 3 (P2)**: Independent - can be implemented in parallel with US4/US5/US6
- **User Story 4 (P2)**: Independent - can be implemented in parallel with US3/US5/US6
- **User Story 5 (P3)**: Independent - can be implemented in parallel with US3/US4/US6
- **User Story 6 (P3)**: Independent - can be implemented in parallel with US3/US4/US5

### Within Each User Story

- Backend agent logic before frontend integration
- MCP tools (in Foundational) before agent implementation
- Database models before services
- Services before API endpoints
- API endpoints before frontend components
- Core implementation before error handling

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003, T004)
- All Foundational tasks marked [P] can run in parallel within Phase 2 (T006-T007, T009-T014, T017-T018)
- Once Foundational phase completes, User Stories 3, 4, 5, 6 can all start in parallel (if team capacity allows)
- All frontend component tasks marked [P] can run in parallel (T030-T032)
- All Polish tasks marked [P] can run in parallel (T062-T072)

---

## Parallel Example: User Story 1 & 2

```bash
# After Foundational phase completes, launch these tasks in parallel:

# Backend agent implementation
Task T019: Implement TodoAgent in src/backend/agents/todo_agent.py

# Frontend components (can run in parallel)
Task T030: Create ChatbotPopup component in src/frontend/components/chat/
Task T031: Create ChatMessage component in src/frontend/components/chat/
Task T032: Create ChatInput component in src/frontend/components/chat/

# Then sequentially:
Task T024: Create chat endpoint in src/backend/api/chat.py (depends on T019)
Task T033: Extend src/frontend/lib/api.ts for chat (depends on T024)
Task T034: Create useChat hook in src/frontend/hooks/ (depends on T033)
Task T035-T036: Add chatbot to Dashboard and Home pages (depends on T030-T034)
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T018) - CRITICAL
3. Complete Phase 3: User Stories 1 & 2 (T019-T040)
4. **STOP and VALIDATE**: Test creating and viewing tasks through chatbot
5. Deploy/demo if ready

**MVP Scope**: 40 tasks (T001-T040)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (T001-T018)
2. Add User Stories 1 & 2 → Test independently → Deploy/Demo (MVP!) (T019-T040)
3. Add User Story 3 → Test independently → Deploy/Demo (T041-T045)
4. Add User Story 4 → Test independently → Deploy/Demo (T046-T050)
5. Add User Story 5 → Test independently → Deploy/Demo (T051-T055)
6. Add User Story 6 → Test independently → Deploy/Demo (T056-T061)
7. Add Polish → Final deployment (T062-T075)

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T018)
2. Once Foundational is done:
   - Developer A: User Stories 1 & 2 (T019-T040)
   - Developer B: User Story 3 (T041-T045) - can start in parallel
   - Developer C: User Story 4 (T046-T050) - can start in parallel
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

**Total Tasks**: 75
- Phase 1 (Setup): 4 tasks
- Phase 2 (Foundational): 14 tasks (BLOCKING)
- Phase 3 (US1 & US2 - MVP): 22 tasks
- Phase 4 (US3): 5 tasks
- Phase 5 (US4): 5 tasks
- Phase 6 (US5): 5 tasks
- Phase 7 (US6): 6 tasks
- Phase 8 (Polish): 14 tasks

**Parallel Opportunities**: 28 tasks marked [P] can run in parallel within their phases

**MVP Scope**: First 40 tasks (T001-T040) deliver create and view functionality

**Independent Stories**: User Stories 3, 4, 5, 6 can all be implemented in parallel after Foundational phase
