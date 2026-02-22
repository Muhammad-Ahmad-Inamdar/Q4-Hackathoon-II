# Implementation Plan: Phase-III Todo AI Chatbot Integration

**Branch**: `007-ai-chatbot-integration` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/007-ai-chatbot-integration/spec.md`

## Summary

Implement an AI-powered chatbot interface that enables users to manage their todos through natural language conversations. The chatbot will appear as a pop-up overlay accessible from Dashboard and Home pages, using Cohere API for natural language understanding and MCP (Model Context Protocol) tools for task operations. The system maintains stateless architecture with conversation history persisted in database, ensuring scalability and reliability.

**Core Value**: Users can create, view, update, complete, and delete tasks conversationally without navigating traditional UI forms, receiving friendly confirmations for all actions.

**Technical Approach**:
- Frontend: React chatbot pop-up component integrated into existing Next.js pages
- Backend: FastAPI REST endpoint for chat processing with stateless request handling
- AI Agent: OpenAI Agents SDK orchestrating Cohere API for NLP and MCP tool invocation
- MCP Server: Expose existing task operations (add_task, list_tasks, update_task, complete_task, delete_task) as MCP tools
- Database: Extend schema with Conversation and Message tables for history persistence

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript/JavaScript (frontend)
**Primary Dependencies**:
- Backend: FastAPI, OpenAI Agents SDK, Cohere Python SDK, SQLModel, Neon PostgreSQL driver
- Frontend: Next.js 14+, React 18+, TailwindCSS, Better Auth client
- MCP: Official MCP SDK (Python)

**Storage**: Neon Serverless PostgreSQL (existing database extended with conversation tables)
**Testing**: pytest (backend), Jest/React Testing Library (frontend), manual integration testing
**Target Platform**:
- Backend: Vercel Serverless Functions (FastAPI)
- Frontend: Vercel (Next.js)
- Database: Neon Serverless PostgreSQL

**Project Type**: Web application (frontend + backend)
**Performance Goals**:
- Chat response time: <5 seconds (P95)
- Conversation history load: <2 seconds
- Support 100+ concurrent chat sessions
- MCP tool execution: <1 second per operation

**Constraints**:
- MUST use Cohere API (no OpenAI API key)
- MUST maintain stateless server architecture
- MUST NOT break existing WebApp UI
- MUST pass user_id explicitly to all MCP tools
- MUST handle all errors gracefully with user-friendly messages

**Scale/Scope**:
- Expected users: 100-1000 concurrent
- Conversation history: Unlimited retention
- Message throughput: 10-50 messages/second peak
- Database: Extend existing schema with 2 new tables

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Reusability ✅
- **Status**: PASS
- **Evidence**: Skills (intent-detection, tool-reasoning, stateless-context-rebuild, etc.) are designed as reusable units. MCP tools are generic and can be used by any agent. Frontend chatbot component can be reused across pages.
- **Validation**: All agents and skills follow reusability principle with clear boundaries.

### II. Statelessness ✅
- **Status**: PASS
- **Evidence**: Server holds no conversation state in memory. All context rebuilt from database on each request. No session variables or global state for conversations.
- **Validation**: Architecture explicitly requires fetching conversation history from DB on every chat request.

### III. Accuracy ✅
- **Status**: PASS
- **Evidence**: All task operations strictly follow MCP tool contracts. Tool schemas define exact input/output formats. Validation enforced at tool boundaries.
- **Validation**: MCP tools have explicit schemas; agent must use exact tool signatures.

### IV. Safety ✅
- **Status**: PASS
- **Evidence**: AI agent restricted to whitelisted MCP tools only. No direct database access. Tool whitelist enforcement prevents hallucination. User_id validation on all operations.
- **Validation**: Tool whitelist defined; no-hallucination-guard skill prevents inventing tools.

### V. User Experience ✅
- **Status**: PASS
- **Evidence**: AI provides friendly confirmations after actions. Error messages are user-friendly without technical details. Conversational tone maintained.
- **Validation**: Response-confirmation skill generates natural language confirmations; error-recovery skill translates technical errors.

### VI. Scalability ✅
- **Status**: PASS
- **Evidence**: Stateless architecture enables horizontal scaling. Database optimized for concurrent access. No single-threaded bottlenecks.
- **Validation**: Stateless design + database indexing + concurrent request support.

### VII. Observability ✅
- **Status**: PASS
- **Evidence**: All MCP tool calls logged. Conversation steps recorded. Tool-call-logging skill captures invocations for audit.
- **Validation**: Logging infrastructure captures tool calls, errors, and conversation events.

**Overall Assessment**: ✅ ALL GATES PASSED - No constitution violations. Architecture aligns with all seven core principles.

## Project Structure

### Documentation (this feature)

```text
specs/007-ai-chatbot-integration/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification (already exists)
├── research.md          # Phase 0 output (research findings)
├── data-model.md        # Phase 1 output (database schema)
├── quickstart.md        # Phase 1 output (setup guide)
├── contracts/           # Phase 1 output (API contracts)
│   ├── chat-api.yaml    # OpenAPI spec for chat endpoint
│   └── mcp-tools.yaml   # MCP tool schemas
├── checklists/          # Quality validation
│   └── requirements.md  # Spec quality checklist (already exists)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (existing structure - INTEGRATE HERE)

```text
src/
├── backend/                     # EXISTING FastAPI backend
│   ├── app/
│   │   ├── main.py             # EXISTING - FastAPI app entry
│   │   ├── database.py         # EXISTING - DB connection
│   │   ├── models.py           # EXISTING - User & Task models
│   │   ├── auth/               # EXISTING - Auth endpoints
│   │   │   ├── router.py
│   │   │   ├── service.py
│   │   │   └── middleware.py
│   │   └── tasks/              # EXISTING - Task CRUD
│   │       ├── router.py
│   │       └── crud.py
│   ├── models/                 # NEW - Add conversation models
│   │   ├── conversation.py     # NEW - Conversation entity
│   │   └── message.py          # NEW - Message entity
│   ├── services/               # NEW - Add chat services
│   │   ├── chat_service.py     # NEW - Chat processing logic
│   │   └── conversation_service.py  # NEW - Conversation persistence
│   ├── api/                    # NEW - Add chat endpoint
│   │   └── chat.py             # NEW - POST /api/{user_id}/chat
│   ├── mcp/                    # NEW - MCP tools
│   │   ├── server.py           # NEW - MCP server setup
│   │   └── tools.py            # NEW - MCP tool definitions
│   └── agents/                 # NEW - AI agent
│       ├── cohere_adapter.py   # NEW - Cohere API integration
│       └── todo_agent.py       # NEW - AI agent orchestration
│
└── frontend/                   # EXISTING Next.js frontend
    ├── app/                    # EXISTING - Next.js App Router
    │   ├── layout.tsx          # EXISTING - Root layout
    │   ├── page.tsx            # EXISTING - Home page (ADD chatbot here)
    │   ├── dashboard/
    │   │   └── page.tsx        # EXISTING - Dashboard (ADD chatbot here)
    │   ├── login/
    │   │   └── page.tsx        # EXISTING - Login page
    │   └── signup/
    │       └── page.tsx        # EXISTING - Signup page
    ├── components/
    │   ├── auth/               # EXISTING - Auth components
    │   ├── tasks/              # EXISTING - Task components
    │   ├── ui/                 # EXISTING - UI components
    │   ├── chat/               # NEW - Add chat components
    │   │   ├── ChatbotPopup.tsx    # NEW - Main chatbot popup
    │   │   ├── ChatMessage.tsx     # NEW - Message display
    │   │   └── ChatInput.tsx       # NEW - Message input
    │   └── AuthProvider.tsx    # EXISTING - Auth context
    ├── lib/
    │   ├── api.ts              # EXISTING - API client (EXTEND for chat)
    │   ├── auth.ts             # EXISTING - Auth helpers
    │   └── types.ts            # EXISTING - Types (EXTEND for chat)
    └── hooks/                  # NEW - Add chat hooks
        └── useChat.ts          # NEW - Chat state management

database/
└── migrations/
    └── 007_add_conversation_tables.sql  # NEW - Migration for conversations & messages
```

**Integration Strategy**:
- Backend: Add new directories (models/, services/, api/, mcp/, agents/) alongside existing app/ directory
- Frontend: Add chat/ components directory and useChat hook, extend existing lib/api.ts
- Database: Extend existing schema with new tables via migration
- NO parallel structure - everything integrates into existing src/ directory

## Complexity Tracking

> **No violations detected - this section intentionally left empty**

All architectural decisions align with constitution principles. No complexity justification required.

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  ┌──────────────┐              ┌──────────────┐            │
│  │  Dashboard   │              │  Home Page   │            │
│  │    Page      │              │              │            │
│  └──────┬───────┘              └──────┬───────┘            │
│         │                              │                     │
│         └──────────┬───────────────────┘                     │
│                    │                                         │
│         ┌──────────▼──────────┐                             │
│         │  ChatbotPopup       │                             │
│         │  Component          │                             │
│         └──────────┬──────────┘                             │
│                    │                                         │
└────────────────────┼─────────────────────────────────────────┘
                     │ REST API
                     │ POST /api/{user_id}/chat
┌────────────────────▼─────────────────────────────────────────┐
│                      Backend (FastAPI)                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Chat Endpoint Handler                    │   │
│  │  1. Validate auth & extract user_id                  │   │
│  │  2. Fetch conversation history from DB               │   │
│  │  3. Reconstruct context (stateless)                  │   │
│  │  4. Invoke AI agent with context + new message       │   │
│  │  5. Persist user message & assistant response        │   │
│  │  6. Return response to frontend                      │   │
│  └────────────┬─────────────────────────────────────────┘   │
│               │                                              │
│  ┌────────────▼─────────────────────────────────────────┐   │
│  │           AI Agent (OpenAI Agents SDK)               │   │
│  │  - Powered by Cohere API                             │   │
│  │  - Intent detection (intent-detection skill)         │   │
│  │  - Tool selection (tool-reasoning skill)             │   │
│  │  - Response generation (response-confirmation skill) │   │
│  └────────────┬─────────────────────────────────────────┘   │
│               │ Tool Invocation                              │
│  ┌────────────▼─────────────────────────────────────────┐   │
│  │              MCP Server                               │   │
│  │  Tools:                                               │   │
│  │  - add_task(user_id, title, description)            │   │
│  │  - list_tasks(user_id, filter)                      │   │
│  │  - update_task(user_id, task_id, title)             │   │
│  │  - complete_task(user_id, task_id)                  │   │
│  │  - delete_task(user_id, task_id)                    │   │
│  └────────────┬─────────────────────────────────────────┘   │
│               │                                              │
└───────────────┼──────────────────────────────────────────────┘
                │
┌───────────────▼──────────────────────────────────────────────┐
│              Database (Neon PostgreSQL)                       │
│  Tables:                                                      │
│  - users (existing)                                          │
│  - tasks (existing)                                          │
│  - conversations (new: user_id, created_at, updated_at)     │
│  - messages (new: conversation_id, role, content, timestamp) │
└───────────────────────────────────────────────────────────────┘
```

### Request Flow (Stateless)

1. **User sends message** in chatbot pop-up
2. **Frontend** calls `POST /api/{user_id}/chat` with message content
3. **Backend endpoint**:
   - Validates JWT token and extracts user_id
   - Fetches conversation history from database (stateless context rebuild)
   - Constructs message array: `[{role: "user", content: "..."}, {role: "assistant", content: "..."}]`
   - Appends new user message to context
4. **AI Agent** (Cohere + OpenAI Agents SDK):
   - Analyzes user intent (intent-detection skill)
   - Selects appropriate MCP tool (tool-reasoning skill)
   - Invokes tool with user_id parameter
   - Generates friendly response (response-confirmation skill)
5. **MCP Tool** executes task operation (e.g., add_task)
6. **Backend**:
   - Persists user message to database
   - Persists assistant response to database
   - Returns response to frontend
7. **Frontend** displays assistant message in chat UI

### Key Design Decisions

| Decision | Option Chosen | Rationale | Alternatives Rejected |
|----------|---------------|-----------|----------------------|
| **Chatbot Placement** | Pop-up overlay | Minimal UI disruption; accessible from multiple pages; non-intrusive | Inline UI (breaks existing layout), Separate page (poor UX) |
| **API Integration** | REST endpoints | Simple, stateless, well-understood; aligns with existing backend | GraphQL (overkill), WebSockets (stateful) |
| **Conversation Persistence** | Database-only | Stateless architecture requirement; single source of truth | In-memory caching (violates statelessness), Redis (adds complexity) |
| **AI Provider** | Cohere API | Requirement to avoid OpenAI API key; cost-effective | OpenAI (violates constraint), Gemini (not specified) |
| **Agent Framework** | OpenAI Agents SDK | Tool calling support; Cohere integration possible | LangChain (heavier), Custom (reinventing wheel) |
| **MCP Implementation** | Official MCP SDK | Standard protocol; reusable tools; clear contracts | Custom protocol (non-standard), Direct function calls (no contracts) |

## Phase 0: Research

**Objective**: Resolve all technical unknowns and validate technology choices.

### Research Tasks

1. **Cohere API Integration with OpenAI Agents SDK**
   - Verify compatibility between OpenAI Agents SDK and Cohere API
   - Document configuration for using Cohere as LLM provider
   - Test tool calling capabilities with Cohere models
   - Identify any limitations or workarounds needed

2. **MCP Tool Schema Design**
   - Research MCP SDK best practices for tool definition
   - Design schemas for 5 task operation tools
   - Validate schema format and parameter types
   - Document error handling patterns

3. **Stateless Conversation Context Reconstruction**
   - Research efficient database query patterns for message history
   - Design indexing strategy for conversation_id and timestamps
   - Validate performance with large conversation histories
   - Document context window limits and truncation strategy

4. **Frontend Chatbot Pop-up Integration**
   - Research React pop-up/modal patterns that don't break existing UI
   - Evaluate z-index layering for pop-up overlay
   - Test responsive design across screen sizes
   - Document integration points with Dashboard and Home pages

5. **Better Auth JWT Validation in Chat Endpoint**
   - Research Better Auth token validation in FastAPI
   - Document user_id extraction from JWT
   - Test authentication flow for chat endpoint
   - Validate session expiry handling

**Output**: `research.md` with findings, code samples, and recommendations for each research task.

## Phase 1: Design & Contracts

**Prerequisites**: Phase 0 research complete

### Data Model Design

**Output**: `data-model.md`

#### New Entities

**Conversation**
- `id` (UUID, primary key)
- `user_id` (UUID, foreign key to users table)
- `created_at` (timestamp with timezone)
- `updated_at` (timestamp with timezone)
- Indexes: `user_id`, `created_at`
- Constraints: user_id must reference existing user

**Message**
- `id` (UUID, primary key)
- `conversation_id` (UUID, foreign key to conversations table)
- `role` (enum: 'user' | 'assistant')
- `content` (text)
- `created_at` (timestamp with timezone)
- Indexes: `conversation_id`, `created_at`
- Constraints: conversation_id must reference existing conversation

#### Existing Entities (Reference)

**Task** (no changes)
- `id`, `user_id`, `title`, `description`, `is_completed`, `created_at`, `updated_at`

**User** (no changes)
- `id`, `email`, `password_hash`, `created_at`

#### Relationships

- User → Conversations (one-to-many)
- Conversation → Messages (one-to-many)
- User → Tasks (one-to-many, existing)

### API Contracts

**Output**: `contracts/chat-api.yaml` (OpenAPI), `contracts/mcp-tools.yaml` (MCP schemas)

#### Chat API Endpoint

```yaml
POST /api/{user_id}/chat
  Parameters:
    - user_id (path, UUID, required)
  Headers:
    - Authorization: Bearer {jwt_token}
  Request Body:
    {
      "message": "string (user's natural language input)",
      "conversation_id": "UUID (optional, for continuing conversation)"
    }
  Response 200:
    {
      "conversation_id": "UUID",
      "response": "string (assistant's response)",
      "timestamp": "ISO 8601 datetime"
    }
  Response 401: Unauthorized
  Response 403: Forbidden (user_id mismatch)
  Response 500: Internal server error
```

#### MCP Tool Schemas

```yaml
add_task:
  input:
    user_id: UUID (required)
    title: string (required, max 200 chars)
    description: string (optional, max 1000 chars)
  output:
    task_id: UUID
    title: string
    created_at: ISO 8601 datetime

list_tasks:
  input:
    user_id: UUID (required)
    filter: enum ['all', 'pending', 'completed'] (optional, default 'all')
  output:
    tasks: array of {id, title, is_completed, created_at}

update_task:
  input:
    user_id: UUID (required)
    task_id: UUID (required)
    title: string (required, max 200 chars)
  output:
    task_id: UUID
    title: string
    updated_at: ISO 8601 datetime

complete_task:
  input:
    user_id: UUID (required)
    task_id: UUID (required)
  output:
    task_id: UUID
    is_completed: boolean
    updated_at: ISO 8601 datetime

delete_task:
  input:
    user_id: UUID (required)
    task_id: UUID (required)
  output:
    success: boolean
    deleted_task_id: UUID
```

### Quickstart Guide

**Output**: `quickstart.md`

Document setup steps for:
1. Environment variables (COHERE_API_KEY, DATABASE_URL, etc.)
2. Database migration execution
3. MCP server startup
4. Backend server startup
5. Frontend development server
6. Testing the chatbot (manual test scenarios)

## Implementation Phases

### Phase 2: Database Schema & Migrations

**Tasks**:
- Create migration file `007_add_conversation_tables.sql`
- Define Conversation and Message tables with proper indexes
- Test migration on development database
- Validate foreign key constraints

**Deliverables**:
- Migration SQL file
- Rollback script
- Migration test results

### Phase 3: MCP Tool Implementation

**Tasks**:
- Implement MCP server using Official MCP SDK
- Define 5 tool schemas (add_task, list_tasks, update_task, complete_task, delete_task)
- Implement tool handlers with user_id validation
- Add tool-call-logging for all invocations
- Write unit tests for each tool

**Deliverables**:
- `src/backend/mcp/server.py`
- `src/backend/mcp/tools.py`
- Tool schema definitions
- Unit tests

**Skills Used**:
- mcp-tool-contracts (enforce schema adherence)
- stateless-db-operations (ensure idempotent operations)
- tool-boundary-definition (separate tool logic from agent logic)

### Phase 4: AI Agent Integration

**Tasks**:
- Configure OpenAI Agents SDK with Cohere API
- Implement intent detection logic
- Implement tool selection and invocation
- Implement response generation with friendly confirmations
- Add error recovery for tool failures
- Test agent with various natural language inputs

**Deliverables**:
- `src/backend/agents/todo_agent.py`
- `src/backend/agents/cohere_adapter.py`
- Agent configuration
- Integration tests

**Skills Used**:
- intent-detection (map NL to intents)
- tool-reasoning (select correct tools)
- response-confirmation (generate friendly responses)
- error-recovery (handle failures gracefully)
- no-hallucination-guard (prevent inventing tools)
- tool-whitelist-enforcement (restrict to approved tools)

### Phase 5: Backend Chat Endpoint

**Tasks**:
- Implement POST /api/{user_id}/chat endpoint
- Add Better Auth JWT validation
- Implement conversation history fetching (stateless context rebuild)
- Integrate AI agent invocation
- Implement message persistence
- Add error handling and logging
- Write API tests

**Deliverables**:
- `src/backend/api/chat.py`
- `src/backend/services/chat_service.py`
- `src/backend/services/conversation_service.py`
- `src/backend/models/conversation.py`
- `src/backend/models/message.py`
- API tests

**Skills Used**:
- stateless-context-rebuild (reconstruct context from DB)
- conversation-persistence (store messages)
- user-intent-safety-check (validate requests)
- ai-boundary-enforcement (prevent out-of-bounds actions)

### Phase 6: Frontend Chatbot Pop-up

**Tasks**:
- Create ChatbotPopup component with responsive design
- Implement chat message display (user and assistant messages)
- Implement message input field with send functionality
- Add loading states and error handling
- Integrate with chat API endpoint
- Add pop-up to Dashboard and Home pages
- Test responsive design across screen sizes
- Write component tests

**Deliverables**:
- `src/frontend/components/chat/ChatbotPopup.tsx`
- `src/frontend/components/chat/ChatMessage.tsx`
- `src/frontend/components/chat/ChatInput.tsx`
- `src/frontend/lib/api.ts` (extend existing for chat)
- `src/frontend/hooks/useChat.ts`
- Component tests

**Skills Used**:
- (Frontend-specific, no backend skills apply)

### Phase 7: Integration Testing & QA

**Tasks**:
- Test all 6 user stories end-to-end
- Test conversation continuity across sessions
- Test error handling (tool failures, invalid commands)
- Test concurrent users and multiple conversations
- Validate logging and observability
- Performance testing (response times, concurrent sessions)
- Security testing (user isolation, auth validation)

**Deliverables**:
- Integration test suite
- Performance test results
- Security audit report
- Bug fixes

**Skills Used**:
- acceptance-criteria-extraction (validate against spec)
- deterministic-behavior-enforcer (ensure reproducibility)

## Testing Strategy

### Functional Testing

**User Story 1: Create Tasks**
- Test: "Add buy groceries" → verify task created
- Test: "I need to call mom" → verify task created with extracted title
- Test: Vague input "do something" → verify clarification request

**User Story 2: View Tasks**
- Test: "Show all my tasks" → verify all tasks displayed
- Test: "What's pending?" → verify only incomplete tasks shown
- Test: No tasks → verify friendly empty state message

**User Story 3: Complete Tasks**
- Test: "Mark buy groceries as complete" → verify task completed
- Test: Non-existent task → verify error message

**User Story 4: Update Tasks**
- Test: "Change buy milk to buy milk and eggs" → verify task updated

**User Story 5: Delete Tasks**
- Test: "Delete the meeting task" → verify task deleted

**User Story 6: Conversation History**
- Test: Close and reopen chatbot → verify messages persist
- Test: Contextual reference "Mark the first one as complete" → verify context understood

### Conversation Continuity Testing

- Multiple conversation threads per user
- Session expiry and re-authentication
- Long conversation histories (100+ messages)
- Concurrent conversations from same user

### Error Handling Testing

- Simulated MCP tool failures
- Cohere API unavailability
- Database connection failures
- Invalid user input
- Malformed requests

### Frontend Testing

- Responsive design on mobile, tablet, desktop
- Pop-up overlay on Dashboard page
- Pop-up overlay on Home page
- Z-index layering with existing UI elements
- Loading states during API calls
- Error message display

### Logging Validation

- All MCP tool calls logged with parameters
- All conversation messages logged
- All errors logged with context
- Log sanitization (no sensitive data)

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Cohere API incompatibility with OpenAI Agents SDK | HIGH | Phase 0 research validates compatibility; fallback to custom agent implementation |
| Performance degradation with large conversation histories | MEDIUM | Implement context window limits; optimize database queries with indexes |
| Pop-up UI conflicts with existing WebApp components | MEDIUM | Thorough z-index testing; CSS isolation; responsive design validation |
| MCP tool failures causing poor UX | MEDIUM | Comprehensive error handling; user-friendly error messages; retry logic |
| Stateless architecture complexity | LOW | Well-documented patterns; stateless-context-rebuild skill provides guidance |
| User isolation vulnerabilities | HIGH | Strict user_id validation on all operations; security testing; auth-context-guard skill |

## Success Metrics

- ✅ All 6 user stories pass acceptance scenarios
- ✅ 90%+ command interpretation accuracy
- ✅ <5 second response time (P95)
- ✅ 100 concurrent sessions supported
- ✅ Zero cross-user data leakage
- ✅ 100% conversation history preservation
- ✅ All MCP tools invoked correctly
- ✅ All errors handled gracefully
- ✅ Pop-up integrates without breaking existing UI
- ✅ All constitutional principles validated

## Next Steps

1. Execute Phase 0 research (generate research.md)
2. Execute Phase 1 design (generate data-model.md, contracts/, quickstart.md)
3. Run `/sp.tasks` to generate implementation tasks
4. Begin Phase 2 implementation (database migrations)
5. Continue through Phases 3-7 sequentially
