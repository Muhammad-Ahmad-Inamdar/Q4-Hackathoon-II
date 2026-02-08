# Data Model: Phase I Todo Console App Extensions

## Task Entity

### Fields
- `id`: string/number - Unique identifier for the task
- `description`: string - Task description text
- `status`: string - Task completion status ("done" or "not done")
- `createdAt`: string - ISO 8601 timestamp when task was created
- `deadline`: string (optional) - ISO 8601 timestamp for task deadline (if specified)

### Validation Rules
- `id` must be unique within the task list
- `description` must not be empty
- `status` must be either "done" or "not done"
- `createdAt` must be a valid ISO 8601 timestamp
- `deadline` must be a valid ISO 8601 timestamp if provided

### State Transitions
- Status can transition from "not done" to "done" (toggle)
- Status can transition from "done" to "not done" (toggle)

## CLI Options Model

### Sorting Options
- `sortBy`: string - Field to sort by ("createdAt", "deadline", "status")
- `order`: string - Sort order ("asc", "desc")

### Filtering Options
- `statusFilter`: string - Filter by status ("done", "not done", null for all)

## Storage Model

### File Structure
- Tasks stored in JSON format in a single file
- Array of task objects with the structure defined above
- File path: `todos.json` (maintaining existing convention)

### Example Structure
```json
[
  {
    "id": "1",
    "description": "Sample task",
    "status": "not done",
    "createdAt": "2026-01-05T10:30:00.000Z",
    "deadline": "2026-01-10T18:00:00.000Z"
  },
  {
    "id": "2",
    "description": "Another task",
    "status": "done",
    "createdAt": "2026-01-05T11:00:00.000Z"
  }
]
```