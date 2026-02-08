# Q4_Hackathon_II--To-Do-App

This is a multi-phase hackathon project to build a comprehensive To-Do application, demonstrating progressive development and learning. This project showcases the evolution from a simple in-memory CLI application to a more sophisticated solution.

## Project Overview

This repository contains a To-Do application developed in 5 phases, each building upon the previous one to demonstrate different concepts and technologies:

- **Phase I**: In-Memory Python Console Todo App
- **Phase II**: [To be implemented]
- **Phase III**: [To be implemented]
- **Phase IV**: [To be implemented]
- **Phase V**: [To be implemented]

## Phase I - In-Memory Python Console Todo App

This is a command-line interface (CLI) application for managing todo tasks. The application runs in memory only and does not persist data beyond the current session.

### Features
- Add new tasks with titles and optional descriptions
- List all tasks with their completion status
- Mark tasks as complete or incomplete
- Update task details
- Delete tasks by ID
- View tasks in a formatted list

### Requirements
- Python 3.7 or higher

### Usage
1. Run the application:
   ```bash
   python src/cli/main.py
   ```

2. Use the following commands:
   - `add <title> [description]` - Add a new task
   - `list` - List all tasks
   - `complete <id>` - Mark task as complete
   - `incomplete <id>` - Mark task as incomplete
   - `update <id> <title> [description]` - Update task details
   - `delete <id>` - Delete a task
   - `help` - Show available commands
   - `quit` or `exit` - Exit the application

### Example Session
```
> add Buy groceries
Added task: 'Buy groceries' with ID 1

> add Call mom Tomorrow is her birthday
Added task: 'Call mom' with ID 2

> list

ID  Status   Title                          Description
----------------------------------------------------------------------
1   ○        Buy groceries
2   ○        Call mom                       Tomorrow is her birthday

> complete 1
Task 1 marked as complete

> list

ID  Status   Title                          Description
----------------------------------------------------------------------
1   ✓        Buy groceries
2   ○        Call mom                       Tomorrow is her birthday

> quit
Goodbye!
```

### Architecture
The application follows a layered architecture:
- **Domain Layer** (`src/todo/models.py`): Contains the Todo entity definition
- **Repository Layer** (`src/todo/repository.py`): Manages in-memory storage of Todo items
- **Service Layer** (`src/todo/services.py`): Orchestrates business operations
- **CLI Layer** (`src/cli/main.py`): Handles user input/output

## Project Structure
```
├── src/
│   ├── todo/
│   │   ├── models.py      # Domain layer
│   │   ├── repository.py  # Repository layer
│   │   └── services.py    # Service layer
│   └── cli/
│       └── main.py        # CLI layer
├── tests/                 # Test files
├── specs/                 # Specification files
├── speckit/              # Specification kit
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── todos.json           # Sample todo data
```

## Future Phases
- **Phase II**: [Details to be added as implemented]
- **Phase III**: [Details to be added as implemented]
- **Phase IV**: [Details to be added as implemented]
- **Phase V**: [Details to be added as implemented]

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
[Specify your license here - e.g., MIT, Apache 2.0, etc.]