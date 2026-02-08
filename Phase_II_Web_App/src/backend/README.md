# Actual Todo App Backend

Complete backend implementation for the todo application with full authentication and task management.

## Features

- ✅ **JWT-based Authentication System**
  - User registration with email/password
  - Secure login with password hashing
  - Token-based authentication for protected endpoints
  - Logout functionality

- ✅ **Full CRUD Operations for Tasks**
  - Create new tasks with title and description
  - Read all user tasks
  - Read specific task by ID
  - Update existing tasks
  - Delete tasks

- ✅ **Security Features**
  - Password hashing with bcrypt
  - JWT token authentication
  - User isolation (users can only access their own tasks)
  - Input validation and sanitization

- ✅ **Database Management**
  - SQLModel ORM
  - SQLite database (configurable)
  - Proper relationships between users and tasks
  - Automatic table creation

- ✅ **CORS Support**
  - Configured for frontend integration
  - Supports localhost:3000 and other common ports

## API Endpoints

### Authentication Endpoints

#### POST `/api/auth/register`
Register a new user
- **Request Body (Form)**: `email`, `password`
- **Response**: JWT token and user info
- **Example**:
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=test@example.com&password=testpass123"
```

#### POST `/api/auth/login`
Login with existing credentials
- **Request Body (Form)**: `email`, `password`
- **Response**: JWT token and user info
- **Example**:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=test@example.com&password=testpass123"
```

#### POST `/api/auth/logout`
Logout (currently just returns success message)
- **Headers**: Authorization: Bearer {token}
- **Response**: Success message

### Task Endpoints (All Require JWT Token)

#### GET `/api/tasks/`
Get all tasks for the authenticated user
- **Headers**: Authorization: Bearer {token}
- **Response**: Array of user's tasks

#### POST `/api/tasks/`
Create a new task
- **Headers**: Authorization: Bearer {token}
- **Request Body (JSON)**: `title` (required), `description` (optional), `completed` (optional)
- **Response**: Created task object

#### GET `/api/tasks/{task_id}`
Get a specific task by ID
- **Headers**: Authorization: Bearer {token}
- **Response**: Task object

#### PUT `/api/tasks/{task_id}`
Update an existing task
- **Headers**: Authorization: Bearer {token}
- **Request Body (JSON)**: Partial task update (`title`, `description`, `completed`)
- **Response**: Updated task object

#### DELETE `/api/tasks/{task_id}`
Delete a task by ID
- **Headers**: Authorization: Bearer {token}
- **Response**: Success message

## Setup

1. Install dependencies:
```bash
pip install fastapi uvicorn sqlmodel bcrypt pyjwt python-multipart
```

2. Start the server:
```bash
python actual_backend.py
```

3. Server will run on `http://localhost:8000`

## Environment Variables

- `BETTER_AUTH_SECRET`: Secret key for JWT signing (defaults to "your-secret-key-change-in-production")
- `DATABASE_URL`: Database connection string (defaults to "sqlite:///actual_todo.db")

## Database Models

### User Model
- `id`: UUID (primary key)
- `email`: String (unique)
- `password`: String (hashed)
- `created_at`: DateTime
- `updated_at`: DateTime

### Task Model
- `id`: UUID (primary key)
- `title`: String
- `description`: String (nullable)
- `completed`: Boolean (default: False)
- `user_id`: UUID (foreign key to User)
- `created_at`: DateTime
- `updated_at`: DateTime

## Security Features

- All passwords are hashed using bcrypt
- JWT tokens expire after 24 hours
- Users can only access their own tasks
- Proper CORS configuration for secure frontend integration
- Input validation and sanitization

## Error Handling

- Proper HTTP status codes (401 for auth, 404 for not found, etc.)
- Descriptive error messages
- Token expiration handling
- Validation error responses