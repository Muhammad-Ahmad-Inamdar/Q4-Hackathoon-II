# Implementation Plan: Database Schema Design

**Branch**: `003-database-schema` | **Date**: 2026-01-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-database-schema/spec.md`

## Summary

Design and implement PostgreSQL database schema using SQLModel ORM with two core entities: User (authentication) and Task (todo items). Enforce user isolation at database level through foreign key constraints and ensure all timestamps use UTC.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: SQLModel, PostgreSQL driver (psycopg2), bcrypt
**Storage**: PostgreSQL (Neon Serverless)
**Testing**: Manual testing with database queries
**Target Platform**: Linux/Windows server
**Project Type**: Web application (backend)
**Performance Goals**: < 50ms average query time
**Constraints**: User isolation mandatory, UTC timestamps only
**Scale/Scope**: Support 1000+ users, 10000+ tasks

## Constitution Check

✅ **PASS**: Spec-Driven Development followed
✅ **PASS**: User isolation enforced at database level
✅ **PASS**: PostgreSQL + SQLModel as mandated
✅ **PASS**: UUID primary keys (not auto-increment)
✅ **PASS**: Password hashing required

## Project Structure

### Documentation (this feature)

```text
specs/003-database-schema/
├── spec.md              # Feature specification
├── plan.md              # This file
└── tasks.md             # Task breakdown
```

### Source Code (repository root)

```text
src/backend/
├── app/
│   ├── models.py        # SQLModel entities (User, Task)
│   ├── database.py      # Database connection and session
│   └── create_db_tables.py  # Table creation script
└── .env                 # DATABASE_URL configuration
```

**Structure Decision**: Backend-only implementation. Models defined in single models.py file for simplicity. Database connection logic separated in database.py.

## Schema Design

### User Table

```python
User:
  - id: str (UUID, primary key)
  - email: str (unique, indexed, not null)
  - password: str (hashed, not null)
  - created_at: datetime (UTC, default now)
  - updated_at: datetime (UTC, default now)
  - last_login_at: datetime (UTC, nullable)
```

### Task Table

```python
Task:
  - id: str (UUID, primary key)
  - user_id: str (foreign key -> User.id, not null)
  - title: str (1-255 chars, not null)
  - description: str (0-1000 chars, nullable)
  - completed: bool (default False)
  - created_at: datetime (UTC, default now)
  - updated_at: datetime (UTC, default now)
```

### Relationships

- User → Task: One-to-Many (one user has many tasks)
- Task → User: Many-to-One (each task belongs to one user)

## Database Connection Strategy

**Connection String Format**: `postgresql://user:password@host:port/database`

**Connection Pooling**: SQLModel default (via SQLAlchemy engine)

**Session Management**: Dependency injection pattern with `get_session()` generator

## Data Validation

**User Entity**:
- Email: Must be valid email format, unique
- Password: Minimum 8 characters (enforced at API level)

**Task Entity**:
- Title: 1-255 characters, required
- Description: 0-1000 characters, optional
- Completed: Boolean, defaults to False

## Migration Strategy

**Phase II Approach**: Direct table creation using `create_tables()` function

**Future**: Use Alembic for proper migrations in production

## Security Considerations

- Passwords NEVER stored in plain text (bcrypt hashing)
- User isolation enforced via foreign key constraints
- Database credentials in .env file (never committed)
- Connection string validation on startup

## Acceptance Criteria

- [ ] User table created with all fields and constraints
- [ ] Task table created with user_id foreign key
- [ ] Database connection established successfully
- [ ] Tables can be queried and data persists
- [ ] User isolation verified (tasks filtered by user_id)
- [ ] Timestamps stored in UTC format
