# Quickstart Guide: Phase I Todo Console App Extensions

## Prerequisites

- Node.js (version compatible with existing project)
- npm or yarn package manager
- Git (for version control)

## Setup

1. Clone the repository (if not already done):
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Verify existing functionality works:
   ```bash
   npm run start
   # or the existing command for the todo app
   ```

## New Features Usage

### 1. CLI Visual Theme
- The application now displays with enhanced colors for better readability
- Colors are automatically applied to all output

### 2. Task Status Toggle
- Toggle task status: `todo toggle <task-id>`
- Changes status from "not done" to "done" or vice versa

### 3. Creation Date Tracking
- All new tasks automatically include creation timestamp
- Creation dates are displayed when listing tasks

### 4. Optional Task Deadline
- Add deadline when creating: `todo add "Task description" --deadline 2026-12-31`
- View deadlines when listing tasks

### 5. Sorting Tasks
- Sort by creation date: `todo list --sort createdAt`
- Sort by deadline: `todo list --sort deadline`
- Sort by status: `todo list --sort status`
- Reverse order: `todo list --sort <field> --order desc`

### 6. Filtering Tasks
- Show only completed tasks: `todo list --done`
- Show only incomplete tasks: `todo list --not-done`

## Implementation Notes

### Code Structure
- New functionality extends existing CLI commands
- Color implementation uses ANSI escape codes
- Task model updated to include creation timestamp and optional deadline
- Sorting and filtering logic added to list functionality

### Files Modified
- `src/models/task.js` - Updated task model to include new fields
- `src/cli/commands.js` - Added new commands and options
- `src/services/taskService.js` - Added sorting and filtering logic
- `src/utils/colors.js` - Added color utilities

### Testing
- Unit tests added for new functionality
- Integration tests for CLI commands
- Backward compatibility verified