<!-- SYNC IMPACT REPORT:
Version change: 1.0.0 → 1.0.0 (initial creation)
Added sections: All sections added as initial constitution
Modified principles: None (new creation)
Removed sections: None
Templates requiring updates: ⚠ pending review of plan-template.md, spec-template.md, tasks-template.md
Follow-up TODOs: None
-->
# Todo App - Phase II Web Application Constitution

## Core Principles

### Spec-Driven Development (Non-Negotiable)
No code is written without a corresponding specification and task. Every feature must be defined in `speckit/specify.md`, every implementation must have a plan in `speckit/plan.md`, every code change must reference a task ID from `speckit/tasks.md`, and all iterations documented in `speckit/phr/` (Phase History Records). Violation means invalid code: code without task reference is rejected, implementation without spec is rejected, changes without plan update are rejected.

### AI-Native Development
Human defines WHAT, AI implements HOW. Claude Code is the primary implementation tool, manual coding is forbidden (except emergency fixes), all agents must follow constitution principles, reusable skills and subagents are encouraged, and vibe coding is prohibited.

### Incremental Implementation
Build incrementally, not sequentially. Never build entire frontend before backend, implement features in thin vertical slices, test each feature end-to-end before moving forward, authentication and complex parts first, fix errors immediately, not later.

### Simplicity and Minimalism
Fewer files, cleaner code, easier maintenance. Consolidate code in same files when logical, no premature abstraction, no duplicate specifications, single source of truth for everything, avoid over-engineering.

### User Data Security
Every user's data is isolated and protected. JWT authentication is mandatory, user isolation is enforced on every endpoint, no shared data between users, no sensitive data in localStorage, environment variables for all secrets.

### Statelessness and Scalability
Every request is independent with no in-memory state (use database), no global variables for user data, JWT tokens carry authentication state, and the system must be scalable and restart-safe.

## Technology Stack Constraints

### Mandatory Technologies
Frontend: Next.js 16+ (App Router only), Frontend Language: TypeScript (Strict mode), Styling: Tailwind CSS, Backend: FastAPI (Python 3.13+), ORM: SQLModel, Database: PostgreSQL (Neon Serverless), Authentication: Better Auth (JWT tokens), Package Managers: uv (backend), npm/pnpm (frontend).

### Forbidden Technologies
No session-based authentication, no SQLAlchemy directly (use SQLModel wrapper), no JavaScript (TypeScript only on frontend), no CSS-in-JS libraries, no localStorage for tokens (HTTP-only cookies or secure headers), no manual SQL queries, no Pages Router (App Router only).

## Architecture Patterns

### User Isolation Pattern
Every database query must filter by user_id. All user-related tables must have `user_id` foreign key, all timestamp fields use UTC, all text fields have max_length limits, and indexes on frequently queried fields.

### API Design Pattern
RESTful conventions strictly followed with specific endpoints: GET `/api/{user_id}/tasks` for listing, POST `/api/{user_id}/tasks` for creation, GET `/api/{user_id}/tasks/{id}` for retrieval, PUT `/api/{user_id}/tasks/{id}` for updates, DELETE `/api/{user_id}/tasks/{id}` for deletion, PATCH `/api/{user_id}/tasks/{id}/complete` for toggling completion status.

### Authentication Flow
Better Auth creates users on signup, generates JWT tokens on login, frontend securely stores tokens, every API request includes Authorization header with Bearer token, backend validates token and extracts user_id, backend filters all queries by user_id.

## Code Quality Standards

### Python Backend Standards
Type safety required with type hints for all function parameters and return values, async/await for all database operations and I/O, proper error handling with HTTPException for API endpoints, structured code following routes → services → repository pattern.

### TypeScript Frontend Standards
Type safety with TypeScript interfaces for all data structures, Server Components by default with Client Components only for interactivity, centralized API client for all backend communication, named exports preferred over default exports for components.

### Documentation Standards
Every module must include purpose, tasks, and spec references in docstring. Every function must include detailed docstring with args, returns, and raises information, with task and spec references.

## Performance and Security Standards

### Performance Targets
API endpoints must respond in < 200ms (95th percentile), database queries in < 50ms average, frontend page load in < 2s (initial), and time to interactive in < 3s.

### Security Requirements
Required environment variables include BETTER_AUTH_SECRET (min 32 chars), JWT_SECRET (min 32 chars), DATABASE_URL, JWT expiration limited to 7 days maximum, HTTP-only cookies preferred for token storage, no tokens in localStorage, proper CORS configuration for local development.

### Data Validation
Backend validation with Pydantic models requiring field constraints, Frontend validation with Zod schemas matching backend constraints, all user inputs must be validated before processing, all database operations must include proper validation.

## Testing and Validation Requirements

### Manual Testing (Mandatory)
Before marking any task complete: test happy path (feature works as expected), test error scenarios (invalid input, unauthorized access), test user isolation (cannot access other users' data), test across browser refresh (state persists).

### Test Scenarios
Authentication: Signup creates new user, Login returns valid JWT, Invalid credentials rejected, Token validation on protected routes. CRUD Operations: Create task saves to database, View tasks shows only user's tasks, Update task modifies database, Delete task removes from database, Mark complete toggles status. User Isolation: User A cannot see User B's tasks, API with wrong user_id returns 401/403, Direct database query shows isolation.

## Environment Configuration

### Required Environment Variables
Frontend (.env.local): BETTER_AUTH_SECRET, BETTER_AUTH_URL, NEXT_PUBLIC_API_URL. Backend (.env): DATABASE_URL, BETTER_AUTH_SECRET, JWT_SECRET, JWT_ALGORITHM, FRONTEND_URL. All secrets in .env files (never committed), .env.example provided with dummy values, environment variables loaded at runtime.

## Project Structure Standard
```
phase-2-web/
│
├── speckit/                    # Spec-Driven Development artifacts
│   ├── specify.md             # WHAT to build
│   ├── plan.md                # HOW to build
│   ├── tasks.md               # Task breakdown
│   ├── implement.md           # Implementation tracking
│   └── phr/                   # Phase History Records
│       ├── iteration-001.md
│       ├── iteration-002.md
│       └── decisions.md
│
├── src/
│   ├── frontend/              # Next.js application
│   │   ├── app/              # App Router pages
│   │   ├── components/       # Reusable components
│   │   ├── lib/              # Utilities and API client
│   │   ├── .env.local        # Frontend environment variables
│   │   └── package.json
│   │
│   └── backend/               # FastAPI application
│       ├── app/
│       │   ├── main.py       # FastAPI entry point
│       │   ├── models.py     # SQLModel database models
│       │   ├── routes/       # API endpoints
│       │   ├── services/     # Business logic
│       │   └── middleware/   # Auth, CORS, etc.
│       ├── .env              # Backend environment variables
│       └── requirements.txt
│
├── .env.example               # Template for all env vars
├── README.md                  # Setup and deployment guide
└── constitution.md            # This file
```

## Success Criteria

### Phase-II is Complete When:
Authentication Works: User can signup and login, JWT tokens issued and validated, Protected routes enforce authentication. CRUD Operations Work: Create, Read, Update, Delete, Toggle all functional, All operations persist to database, All operations respect user isolation. Integration Works: Frontend successfully calls backend APIs, CORS configured correctly, JWT tokens flow properly, Errors handled gracefully. Code Quality: All code references task IDs, Type safety throughout, Constitution principles followed, Documentation complete. Deliverables: GitHub repository public, Application deployed on Vercel, Backend API accessible, Demo video recorded (< 90 seconds), README with setup instructions.

### Failure Modes Prevention
Frontend-Backend Communication Failure: Configure CORS properly from start, test API connectivity before building features, use centralized API client with error handling. Better Auth Integration Issues: Use same `BETTER_AUTH_SECRET` in both, implement token validation early, test authentication flow before CRUD features. Database Connection Issues: Verify `DATABASE_URL` format immediately, test database connection on startup, use connection pooling. User Isolation Failures: Always filter by `user_id` in queries, test with multiple users, validate `user_id` matches token.

## Agent Coordination

### Main Orchestrator Agent Responsibilities
Ensure spec-driven workflow followed, coordinate all subagents, break down complex tasks, validate all work against constitution.

### Specialized Agents
Frontend Engineer: Next.js, React, Better Auth UI. Backend Engineer: FastAPI, SQLModel, JWT validation. Database Architect: Schema design, indexes, migrations. Integration Specialist: Frontend-Backend-Auth connectivity. QA Tester: End-to-end testing, user isolation validation.

All agents must reference this constitution before every action, work only on tasks from `speckit.tasks`, document work in appropriate speckit files, validate work against success criteria.

## Governance

This constitution is MANDATORY for all AI agents (Claude Code, subagents, skills), all code contributions, all specification documents, all implementation work. Violation Consequences: Code rejected, Task marked incomplete, Re-implementation required. Amendment procedure: Identify need for change, Document reason in `speckit/phr/decisions.md`, Update constitution, Increment version number, Notify all agents.

**Version**: 1.0.0 | **Ratified**: 2026-01-30 | **Last Amended**: 2026-01-30