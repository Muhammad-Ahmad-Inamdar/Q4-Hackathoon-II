---
id: 001
title: Create Phase-III Constitution
stage: constitution
date: 2026-02-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 007-ai-chatbot-integration
user: user
command: /sp.constitution
labels: ["constitution", "governance", "phase-iii", "ai-chatbot"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

Constitution
=============

/sp.constitution

Project: Phase-III Todo AI Chatbot — Spec-Driven Integration with WebApp

Core principles:
- Reusability: Skills and agents are reusable across multiple tasks and future projects
- Statelessness: Server holds no conversation state; all context is rebuilt per request
- Accuracy: All task operations must strictly follow MCP tool contracts
- Safety: AI cannot perform actions outside defined tool boundaries or hallucinate
- User Experience: Responses must be clear, friendly, and confirm executed actions
- Scalability: Architecture supports horizontal scaling and multi-threaded access
- Observability: All tool calls and conversation steps are logged for audit and debugging

Key standards:
- Agents interact only via MCP tools; direct DB access by AI is prohibited
- Conversation state persists exclusively in the database
- API integrations between frontend and backend are RESTful and consistent
- Frontend chatbot shows as a pop-up accessible from main UI pages (Dashboard + Home)
- Error handling is user-friendly and prevents exposing internal system details
- Chatbot leverages Coher API, not OpenAI API key

Constraints:
- Frontend integration must not break existing WebApp UI
- Must support all existing todo features: create, list, update, complete, delete, tagging
- Must handle simultaneous users and multiple conversation threads
- Must deploy using Vercel (frontend) + FastAPI backend + MCP + Coher API

Success criteria:
- AI can fully manage todos through natural language
- Conversation state persists correctly across sessions
- Chatbot behaves deterministically per spec
- Zero unsafe or out-of-bound AI actions
- Frontend pop-up is responsive and accessible on all main pages

## Response snapshot

Created Phase-III Todo AI Chatbot Constitution v1.0.0 at `.specify/memory/constitution.md`.

The constitution establishes 7 core principles:
1. Reusability - Skills and agents as reusable intelligence units
2. Statelessness - No in-memory conversation state
3. Accuracy - Strict MCP tool contract adherence
4. Safety - AI boundary enforcement and no hallucination
5. User Experience - Clear, friendly confirmations
6. Scalability - Horizontal scaling support
7. Observability - Comprehensive logging and audit trails

Technical standards defined for:
- Agent-Tool Interaction (MCP-only, explicit user_id)
- Data Persistence (database as single source of truth)
- API Design (RESTful, consistent)
- Frontend Integration (pop-up on Dashboard/Home)
- Error Handling (user-friendly, no stack traces)
- AI Provider (Cohere API, not OpenAI)

Deployment constraints specified:
- Vercel (frontend) + FastAPI (backend) + MCP + Cohere
- Support all existing todo features
- Handle concurrent users and multiple conversations

Success criteria and governance rules established with semantic versioning policy.

## Outcome

- ✅ Impact: Established foundational governance for Phase-III AI chatbot development
- 🧪 Tests: No tests (governance document)
- 📁 Files: Created .specify/memory/constitution.md (175 lines)
- 🔁 Next prompts: /sp.specify to create feature specification, /sp.plan for architecture
- 🧠 Reflection: Constitution provides clear boundaries for AI behavior, stateless architecture requirements, and reusability mandates that will guide all Phase-III implementation work

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (governance document)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate constitution principles during first feature specification
