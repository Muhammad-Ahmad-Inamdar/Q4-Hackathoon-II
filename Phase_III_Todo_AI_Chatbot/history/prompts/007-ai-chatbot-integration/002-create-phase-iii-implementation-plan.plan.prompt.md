---
id: 001
title: Create Phase-III Implementation Plan
stage: plan
date: 2026-02-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: 007-ai-chatbot-integration
branch: 007-ai-chatbot-integration
user: user
command: /sp.plan
labels: ["plan", "phase-iii", "ai-chatbot", "architecture", "mcp", "cohere"]
links:
  spec: specs/007-ai-chatbot-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/007-ai-chatbot-integration/plan.md
  - specs/007-ai-chatbot-integration/research.md
  - specs/007-ai-chatbot-integration/data-model.md
  - specs/007-ai-chatbot-integration/contracts/chat-api.yaml
  - specs/007-ai-chatbot-integration/contracts/mcp-tools.yaml
  - specs/007-ai-chatbot-integration/quickstart.md
tests:
  - none
---

## Prompt

Plan
====
/sp.plan

Create:
- Architecture sketch: Frontend pop-up integrated into main pages, FastAPI backend, MCP server exposing tools, Cohere API-powered agent
- Section structure: 1) Chatbot UI/UX, 2) MCP tool definitions, 3) Agent behavior, 4) Database persistence, 5) Error handling
- Research approach: Evaluate Cohere API for task NLP, map intents to MCP tool calls
- Quality validation: Test all task operations with multiple scenarios and edge cases

Decisions needing documentation:
- Chatbot placement: Pop-up vs inline UI → chosen pop-up for minimal UI disruption
- API integration: REST endpoints between frontend and backend → chosen for simplicity & statelessness
- Conversation persistence: DB-only vs memory caching → DB-only for stateless design
- Model usage: Cohere API agent vs Gemini/OpenAI → Cohere API chosen to avoid OpenAI API key

Testing strategy:
- Functional testing: Create, list, update, complete, delete tasks
- Conversation continuity: Multiple threads, user sessions
- Error handling: Simulated tool failures, invalid commands
- Frontend: Responsiveness across pages and screen sizes
- Logging: Validate all tool calls and conversation events recorded

Technical details:
- Use research-concurrent approach: Implement while testing Cohere API flows
- Organize by phases: Design → Agent Integration → Frontend Pop-up → Backend MCP Integration → Testing & QA
- Follow standards from Constitution (reusability, statelessness, safety)
- Document all decisions, tool boundaries, and skill usages

## Response snapshot

Created comprehensive implementation plan for Phase-III Todo AI Chatbot Integration with complete Phase 0 (Research) and Phase 1 (Design) artifacts.

**Main Plan Document** (`plan.md`):
- Architecture overview with system component diagram
- Request flow for stateless processing
- Constitution check (all 7 principles validated ✅)
- Project structure (backend, frontend, database, MCP)
- Key design decisions documented with rationale
- Implementation phases (2-7) defined
- Testing strategy and risk assessment
- Success metrics aligned with spec

**Phase 0: Research** (`research.md`):
- Cohere API integration with OpenAI Agents SDK (custom adapter approach)
- MCP tool schema design with JSON Schema validation
- Stateless conversation context reconstruction (database query patterns)
- Frontend chatbot pop-up integration (z-index strategy, responsive design)
- Better Auth JWT validation in FastAPI (middleware pattern)
- Technology stack summary and risk mitigation

**Phase 1: Design** (`data-model.md`):
- New entities: Conversation, Message (with full schema definitions)
- Database migration SQL with indexes and triggers
- SQLModel definitions for Python ORM
- Query patterns for stateless context rebuild
- Performance considerations and security guidelines

**API Contracts**:
- `chat-api.yaml`: OpenAPI 3.0 spec for POST /api/{user_id}/chat endpoint
- `mcp-tools.yaml`: Complete schemas for 5 MCP tools (add_task, list_tasks, update_task, complete_task, delete_task)

**Quickstart Guide** (`quickstart.md`):
- Environment configuration (backend and frontend)
- Database migration steps
- Dependency installation
- Server startup instructions
- Manual testing scenarios
- Troubleshooting guide
- Production deployment checklist

**Key Architectural Decisions**:
1. Pop-up overlay for chatbot (minimal UI disruption)
2. REST API for frontend-backend communication (stateless, simple)
3. Database-only persistence (no caching, stateless architecture)
4. Cohere API with custom adapter (requirement compliance)
5. MCP tools for all task operations (reusability, safety)

**Constitution Compliance**: All 7 principles validated and documented in plan.

## Outcome

- ✅ Impact: Complete implementation plan with research, design, and contracts ready for task generation
- 🧪 Tests: No tests (planning artifacts)
- 📁 Files: Created 6 planning documents (plan, research, data-model, 2 contracts, quickstart)
- 🔁 Next prompts: /sp.tasks to generate implementation tasks from plan
- 🧠 Reflection: Plan successfully addresses all technical unknowns through Phase 0 research. Phase 1 design provides complete database schema, API contracts, and setup guide. Architecture follows constitutional principles (statelessness, safety, reusability). Ready for task generation and implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution Check - PASS (all 7 principles)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate Cohere-OpenAI SDK adapter implementation in Phase 3
