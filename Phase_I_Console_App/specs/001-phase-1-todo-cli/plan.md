# Implementation Plan: Phase I - In-Memory Python Console Todo App

**Feature**: 001-phase-1-todo-cli
**Created**: 2026-01-04
**Status**: Draft
**Specification Reference**: spec.md

## Architecture Overview

This plan defines the technical implementation of the Phase I Todo CLI application following the layered architecture pattern:

### Layered Architecture
1. **Domain Layer** (`src/todo/models.py`)
   - Contains the core Todo entity definition
   - Implements business rules and validation
   - Independent of UI or storage concerns

2. **Repository Layer** (`src/todo/repository.py`)
   - Manages in-memory storage of Todo items
   - Handles CRUD operations for tasks
   - Responsible for ID generation and uniqueness

3. **Service Layer** (`src/todo/services.py`)
   - Orchestrates business operations
   - Mediates between CLI and repository
   - Enforces application-level business rules

4. **CLI Layer** (`src/cli/main.py`)
   - Handles user input/output
   - Provides command-line interface
   - Translates user actions to service calls

## Technical Specifications

### Domain Layer Implementation
- **File**: `src/todo/models.py`
- **Purpose**: Define the Todo entity with all required attributes
- **Attributes**:
  - `id` (int): Unique auto-generated identifier
  - `title` (str): Required task title
  - `description` (str): Optional task description
  - `completed` (bool): Task completion status (default: False)
- **Methods**:
  - `complete()`: Mark task as complete
  - `incomplete()`: Mark task as incomplete
  - `update()`: Update task details

### Repository Layer Implementation
- **File**: `src/todo/repository.py`
- **Purpose**: In-memory storage and retrieval of Todo items
- **Storage**: Python list/dict for storing Todo objects
- **Operations**:
  - `add(todo)`: Add a new todo
  - `get_by_id(id)`: Retrieve a todo by ID
  - `get_all()`: Retrieve all todos
  - `update(todo)`: Update an existing todo
  - `delete(id)`: Delete a todo by ID
  - `get_by_status(status)`: Filter todos by completion status

### Service Layer Implementation
- **File**: `src/todo/services.py`
- **Purpose**: Business logic orchestration
- **Operations**:
  - `add_task(title, description)`: Create and add a new task
  - `get_all_tasks()`: Retrieve all tasks
  - `get_task_by_id(id)`: Retrieve specific task
  - `update_task(id, title, description)`: Update task details
  - `complete_task(id)`: Mark task as complete
  - `incomplete_task(id)`: Mark task as incomplete
  - `delete_task(id)`: Delete a task
  - `get_tasks_by_status(status)`: Filter tasks by status

### CLI Layer Implementation
- **File**: `src/cli/main.py`
- **Purpose**: Command-line interface for user interaction
- **Features**:
  - Menu-driven interface
  - Command parsing for add, list, update, delete, complete operations
  - Error handling and user feedback
  - Continuous execution loop until user exits

## Implementation Strategy

### Phase 1: Core Domain Setup
1. **Create project structure**:
   - `src/todo/__init__.py`
   - `src/cli/__init__.py`
   - Setup directories as specified

2. **Implement Domain Layer**:
   - Create `src/todo/models.py`
   - Define Todo class with required attributes
   - Implement validation and state change methods

### Phase 2: Storage Layer
1. **Implement Repository Layer**:
   - Create `src/todo/repository.py`
   - Implement in-memory storage operations
   - Handle ID generation and uniqueness
   - Implement filtering capabilities

### Phase 3: Business Logic
1. **Implement Service Layer**:
   - Create `src/todo/services.py`
   - Implement service methods that map to functional requirements
   - Connect services to repository
   - Add error handling and validation

### Phase 4: User Interface
1. **Implement CLI Layer**:
   - Create `src/cli/main.py`
   - Implement menu system
   - Add command parsing
   - Connect CLI to service layer
   - Implement error handling and user feedback

## Implementation Tasks Mapping

### From Specification Requirements:

**FR-001: System MUST allow users to add new tasks with a required title and optional description**
- Implementation: `services.add_task()` and CLI command
- Files: `src/todo/services.py`, `src/cli/main.py`

**FR-002: System MUST assign each task a unique, auto-generated ID**
- Implementation: Repository handles ID generation
- Files: `src/todo/repository.py`

**FR-003: System MUST mark newly added tasks as incomplete by default**
- Implementation: Todo model default value
- Files: `src/todo/models.py`

**FR-004: Users MUST be able to view all tasks with their ID, title, and completion status**
- Implementation: `services.get_all_tasks()` and CLI display
- Files: `src/todo/services.py`, `src/cli/main.py`

**FR-005: System MUST allow users to update task title and description by ID**
- Implementation: `services.update_task()` and CLI command
- Files: `src/todo/services.py`, `src/cli/main.py`

**FR-006: System MUST preserve task completion status when updating task details**
- Implementation: Update method preserves status
- Files: `src/todo/models.py`, `src/todo/services.py`

**FR-007: Users MUST be able to delete tasks by ID**
- Implementation: `services.delete_task()` and CLI command
- Files: `src/todo/services.py`, `src/cli/main.py`

**FR-008: System MUST allow users to mark tasks as complete or incomplete by ID**
- Implementation: `services.complete_task()`/`incomplete_task()` and CLI commands
- Files: `src/todo/services.py`, `src/cli/main.py`

**FR-009: System MUST reflect updated task status when displaying the task list**
- Implementation: Display methods show current status
- Files: `src/cli/main.py`

**FR-010: System MUST maintain all tasks in memory during the current session**
- Implementation: In-memory storage in repository
- Files: `src/todo/repository.py`

**FR-011: System MAY store tasks in a single local file for state restoration between runs**
- Implementation: File persistence in repository layer
- Files: `src/todo/repository.py`

**FR-012: System MUST load tasks from the local file on application start if it exists**
- Implementation: File loading in repository initialization
- Files: `src/todo/repository.py`

**FR-013: System MUST save the current in-memory task state to the local file on application exit**
- Implementation: File saving in repository shutdown
- Files: `src/todo/repository.py`

**FR-014: The local file format MUST be simple and human-readable (e.g., JSON)**
- Implementation: JSON serialization in repository
- Files: `src/todo/repository.py`

**FR-015: The local file is NOT a database and MUST NOT be treated as one**
- Implementation: Simple file operations, not database-like queries
- Files: `src/todo/repository.py`

## Quality Assurance

### Code Quality Standards
- Follow Python PEP 8 style guidelines
- Include type hints for all function parameters and return values
- Add docstrings for all public methods and classes
- Maintain clean separation between layers

### Error Handling
- Validate input parameters before processing
- Provide clear error messages to users
- Handle edge cases gracefully (e.g., invalid task IDs)
- Maintain application stability during errors

### Testing Approach
- Unit tests for each layer (domain, repository, service)
- Integration tests for CLI functionality
- Manual testing of all user flows

## Success Criteria for Implementation

### Technical Completion
- [ ] All four layers implemented as specified
- [ ] All functional requirements from spec implemented
- [ ] Clean separation of concerns maintained
- [ ] Code follows Python best practices

### Functional Completion
- [ ] Users can add tasks with title and optional description
- [ ] Tasks are assigned unique, auto-generated IDs
- [ ] Newly added tasks are marked as incomplete by default
- [ ] Users can view all tasks with ID, title, and status
- [ ] Users can update task details while preserving status
- [ ] Users can delete tasks by ID
- [ ] Users can mark tasks as complete/incomplete by ID
- [ ] Status changes are reflected in task lists
- [ ] All tasks exist in memory during session
- [ ] Tasks can be saved to a local file on exit
- [ ] Tasks can be loaded from a local file on startup
- [ ] Local file uses simple, human-readable format (JSON)

### Quality Completion
- [ ] Proper error handling implemented
- [ ] User-friendly CLI interface
- [ ] Application runs continuously until user exits
- [ ] All code traces back to approved tasks