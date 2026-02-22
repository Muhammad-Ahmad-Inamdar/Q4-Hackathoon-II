# Testing Guide - Phase III AI Chatbot

## Prerequisites

1. **Cohere API Key**: Get from https://dashboard.cohere.com/api-keys
2. **Database**: Neon PostgreSQL (already configured)
3. **Environment Variables**: Already configured

## Backend Testing

### 1. Start Backend Server

```bash
cd "E:\MOHAMMAD AHMAD\Courses\Governor Sindh IT\Q4\Hackathon_02\Phase_III_Todo_AI_Chatbot\src\backend"

# Activate virtual environment (if using one)
# python -m venv venv
# venv\Scripts\activate

# Start server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 2. Test Health Endpoint

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "cors_enabled": true,
  "allowed_origins": [...]
}
```

### 3. Test Chat Endpoint (Manual)

First, login to get JWT token:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

Then test chat:
```bash
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"message":"Add buy groceries to my list"}'
```

**Expected Response:**
```json
{
  "conversation_id": "uuid",
  "response": "Task 'Buy groceries' created successfully!",
  "timestamp": "2026-02-09T..."
}
```

## Frontend Testing

### 1. Start Frontend Server

```bash
cd "E:\MOHAMMAD AHMAD\Courses\Governor Sindh IT\Q4\Hackathon_02\Phase_III_Todo_AI_Chatbot\src\frontend"

# Install dependencies (if needed)
npm install

# Start dev server
npm run dev
```

**Expected Output:**
```
ready - started server on 0.0.0.0:3000
```

### 2. Test in Browser

1. **Open**: http://localhost:3000
2. **Login**: Use existing credentials or create new account
3. **Navigate**: Go to Dashboard
4. **Look for**: Blue floating button in bottom-right corner
5. **Click**: Open chatbot popup

### 3. Test User Story 1: Create Tasks

Try these commands in chatbot:
- "Add buy groceries"
- "Create task: Call mom tonight"
- "I need to finish the project report"

**Expected Behavior:**
- Chatbot shows "thinking" animation
- Response confirms task creation
- Task appears in main task list

### 4. Test User Story 2: View Tasks

Try these commands:
- "Show me all my tasks"
- "What do I need to do?"
- "What have I finished?"

**Expected Behavior:**
- Chatbot lists your tasks
- Shows task titles and completion status
- Friendly formatting

## Manual Test Scenarios

### Scenario 1: First-Time User
1. Create new account
2. Open chatbot
3. See welcome message
4. Type "Add buy milk"
5. Verify task created
6. Type "Show my tasks"
7. Verify task listed

### Scenario 2: Conversation Continuity
1. Open chatbot
2. Type "Add task 1"
3. Type "Add task 2"
4. Close chatbot
5. Reopen chatbot
6. Verify previous messages visible
7. Type "Show my tasks"
8. Verify both tasks listed

### Scenario 3: Error Handling
1. Open chatbot
2. Type empty message (should be disabled)
3. Type very long message (should work)
4. Type nonsense "asdfghjkl" (should get helpful response)

### Scenario 4: Multiple Pages
1. Test chatbot on Dashboard page
2. Navigate to Home page
3. Verify chatbot still works
4. Verify conversation continues

## Troubleshooting

### Backend Issues

**Error: "COHERE_API_KEY not found"**
- Solution: Add valid Cohere API key to `src/backend/.env`

**Error: "relation 'conversations' does not exist"**
- Solution: Run migration again: `python run_migration.py`

**Error: "Module not found"**
- Solution: Install dependencies: `pip install -r requirements.txt`

### Frontend Issues

**Error: "Cannot find module '@/components/chat'"**
- Solution: Restart Next.js dev server

**Chatbot not appearing**
- Check: User is authenticated
- Check: JWT token exists in localStorage
- Check: Console for errors

**API calls failing**
- Check: Backend server is running
- Check: NEXT_PUBLIC_API_URL is correct
- Check: CORS is configured properly

## Success Criteria

✅ Backend server starts without errors
✅ Chat endpoint responds to requests
✅ Frontend compiles without errors
✅ Chatbot popup appears on Dashboard
✅ Can create tasks via natural language
✅ Can view tasks via natural language
✅ Conversation history persists
✅ Error messages are user-friendly

## Next Steps After Testing

1. **Fix any bugs** found during testing
2. **Implement User Stories 3-6** (complete, update, delete, history)
3. **Deploy to production**
4. **Monitor logs** for issues
5. **Gather user feedback**
