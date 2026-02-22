# Todo App - Phase II Web Application

A secure, multi-user todo application with authentication and CRUD operations.

## Features

- User authentication (signup/login/logout)
- Create, read, update, and delete tasks
- Mark tasks as complete/incomplete
- User isolation (users can only see their own tasks)
- Responsive design with Tailwind CSS

## Tech Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.13+, SQLModel
- **Database**: PostgreSQL (Neon Serverless)
- **Authentication**: Better Auth with JWT tokens

## Setup Instructions

### Prerequisites

- Node.js 18+
- Python 3.13+
- PostgreSQL database (or Neon account)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd src/backend
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the environment file and update the values:
```bash
cp .env.example .env
```

5. Run the application:
```bash
python -m uvicorn app.main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd src/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Copy the environment file and update the values:
```bash
cp .env.example .env.local
```

4. Run the development server:
```bash
npm run dev
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login a user
- `POST /api/auth/logout` - Logout a user

### Tasks
- `GET /api/tasks/` - Get all tasks for the authenticated user
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a task
- `DELETE /api/tasks/{task_id}` - Delete a task
- `PATCH /api/tasks/{task_id}/toggle-completion` - Toggle task completion status

## Environment Variables

### Backend (.env)
- `DATABASE_URL` - PostgreSQL database connection string
- `BETTER_AUTH_SECRET` - Secret key for JWT signing

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL` - Base URL for the backend API

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License.