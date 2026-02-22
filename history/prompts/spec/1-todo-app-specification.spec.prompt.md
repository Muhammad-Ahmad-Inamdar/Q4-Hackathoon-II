---
id: 1
title: "Todo App Phase II Specification"
stage: spec
date: 2026-01-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: "todo-app-phase-ii"
branch: "master"
user: "user"
command: "/sp.specify"
labels: ["specification", "todo-app", "full-stack", "authentication"]
links:
  spec: "speckit/specify.md"
  ticket: null
  adr: null
  pr: null
files:
  - "speckit/specify.md"
tests: []
prompt_text: |
  # Specification: Phase-II Full-Stack Todo Web App

  ## Project Goal
  Build a secure, multi-user web application for task management with authentication and CRUD operations.

  ---

  ## Success Criteria

  **Phase-II is complete when:**
  1. ✅ Users can signup/login with JWT authentication
  2. ✅ Users can Create, Read, Update, Delete, and Toggle tasks
  3. ✅ Frontend communicates with backend (no CORS errors)
  4. ✅ All data persists in Neon PostgreSQL
  5. ✅ User data isolation enforced (User A can't see User B's tasks)

  ---

  ## Features (Basic Level Only)

  ### Authentication
  - **F-001:** User signup with email/password
  - **F-002:** User login with JWT token generation
  - **F-003:** User logout (clear token)
  - **F-004:** Session persistence across page refreshes

  ### Task Management
  - **F-005:** Create task (title required, description optional)
  - **F-006:** View all tasks (user's tasks only)
  - **F-007:** View single task details
  - **F-008:** Update task (title and/or description)
  - **F-009:** Delete task (permanent)
  - **F-010:** Toggle task complete/incomplete

  ---

  ## Technology Stack

  | Component | Technology | Version |
  |-----------|-----------|---------|
  | Frontend | Next.js | 16+ (App Router) |
  | Frontend Language | TypeScript | Latest (strict) |
  | Styling | Tailwind CSS | Latest |
  | Backend | FastAPI | Latest |
  | Backend Language | Python | 3.13+ |
  | ORM | SQLModel | Latest |
  | Database | PostgreSQL | Neon Serverless |
  | Authentication | Better Auth | Latest (JWT) |

  ---

  ## API Endpoints

  | Method | Endpoint | Purpose | Auth |
  |--------|----------|---------|------|
  | POST | `/api/auth/signup` | Create account | No |
  | POST | `/api/auth/login` | Get JWT token | No |
  | GET | `/api/{user_id}/tasks` | List all tasks | Yes |
  | POST | `/api/{user_id}/tasks` | Create task | Yes |
  | GET | `/api/{user_id}/tasks/{id}` | Get task details | Yes |
  | PUT | `/api/{user_id}/tasks/{id}` | Update task | Yes |
  | DELETE | `/api/{user_id}/tasks/{id}` | Delete task | Yes |
  | PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle complete | Yes |

  ---

  ## Database Schema

  ### Users Table (Better Auth managed)
  ```sql
  CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```

  ### Tasks Table
  ```sql
  CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

  CREATE INDEX idx_tasks_user_id ON tasks(user_id);
  ```

  ---

  ## Environment Variables

  ### Frontend (`.env.local`)
  ```bash
  BETTER_AUTH_SECRET=your-secret-32-chars-min
  BETTER_AUTH_URL=http://localhost:3000
  NEXT_PUBLIC_API_URL=http://localhost:8000
  ```

  ### Backend (`.env`)
  ```bash
  DATABASE_URL=postgresql://user:pass@host/db
  BETTER_AUTH_SECRET=same-as-frontend
  JWT_SECRET=your-jwt-secret-32-chars-min
  FRONTEND_URL=http://localhost:3000
  ```

  ---

  ## User Interface

  ### Pages
  1. **Signup Page** (`/signup`) - Email/password registration
  2. **Login Page** (`/login`) - Email/password authentication
  3. **Task List** (`/tasks`) - Main dashboard with all tasks
  4. **Create/Edit Modal** - Overlay for task creation/editing

  ### Key UI Elements
  - Task list with checkboxes, edit, and delete buttons
  - "Add Task" button (top-right)
  - User email and logout button (header)
  - Empty state: "No tasks yet"
  - Loading indicators during API calls
  - Error messages for failures

  ---

  ## Core Requirements

  ### Security
  - JWT tokens expire in 7 days
  - All queries filtered by `user_id`
  - Passwords hashed (never stored plain)
  - CORS configured for frontend-backend communication

  ### Performance
  - API response < 200ms (95th percentile)
  - Page load < 2 seconds
  - Database queries indexed on `user_id`

  ### Code Quality
  - All code references task IDs in comments
  - Type safety (TypeScript + Python type hints)
  - No hardcoded secrets (use env vars)
  - Follows constitution principles

  ---

  ## Out of Scope (Not Phase-II)

  ❌ Task priorities, tags, categories
  ❌ Search and filtering
  ❌ Recurring tasks
  ❌ Due dates and reminders
  ❌ AI chatbot interface
  ❌ Real-time collaboration
  ❌ Email notifications
  ❌ Docker/Kubernetes deployment

  ---

  ## Acceptance Tests

  ### Test Scenario 1: New User Journey
  1. User signs up → automatically logged in
  2. User creates first task → appears in list
  3. User refreshes page → still logged in, task visible

  ### Test Scenario 2: CRUD Operations
  1. User creates 3 tasks
  2. User marks one complete
  3. User edits another
  4. User deletes the third
  5. All changes persist after logout/login

  ### Test Scenario 3: User Isolation
  1. User A creates tasks, logs out
  2. User B signs up, sees empty list (not User A's tasks)
  3. User B creates own tasks
  4. User A logs back in, sees only their tasks

  ---

  ## Deliverables

  - [ ] Public GitHub repository
  - [ ] Frontend deployed on Vercel
  - [ ] Backend deployed (Render/Railway/similar)
  - [ ] Database on Neon
  - [ ] Demo video (< 90 seconds)
  - [ ] README with setup instructions
  - [ ] All speckit files (specify, plan, tasks, implement)

  ---

  ## Timeline

  **Submission Deadline:** Sunday, December 14, 2025
  **Points:** 150/1000

  **Development Approach:**
  1. Week 1: Auth setup (signup/login working)
  2. Week 2: CRUD implementation (one feature at a time)
  3. Week 3: Integration & testing
  4. Week 4: Deployment & documentation

  ---

  ## Known Risks & Mitigation

  **Risk:** Better Auth integration fails
  **Mitigation:** Implement auth FIRST, test thoroughly before CRUD

  **Risk:** Frontend-Backend connection issues
  **Mitigation:** Configure CORS from day 1, test API immediately

  **Risk:** User isolation failure
  **Mitigation:** Always filter by user_id, test with multiple users

  ---

  **Status:** Draft - Ready for Review
  **Next:** Create plan.md → tasks.md → implement

  **Approval:** ⬜ Approved | ⬜ Needs Revision

response_text: |
  I've created the specification file based on your description. The spec outlines the Todo App - Phase II Full-Stack Web Application with all the required functionality including user authentication, task management CRUD operations, and user data isolation.

  The specification includes:
  - Detailed functional requirements
  - User scenarios
  - Success criteria
  - Technical requirements
  - Security considerations
  - Testing requirements
  - And all other necessary sections

outcome: "Specification document created successfully at speckit/specify.md following the SpeckitPlus methodology."
evaluation: "The specification comprehensively covers all requirements from the user input, including authentication, task management, security, and technical constraints."
---