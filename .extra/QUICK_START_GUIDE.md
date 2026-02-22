# Phase-III Chatbot - Quick Start Guide 🚀

## Prerequisites ✅

Before running the chatbot, ensure you have:

1. **Cohere API Key** - Get from https://dashboard.cohere.com/api-keys
2. **Database** - Neon PostgreSQL (already configured for Phase-II)
3. **Node.js 18+** - For frontend
4. **Python 3.13+** - For backend

---

## 📋 Quick Setup (5 Minutes)

### Step 1: Backend Configuration

```bash
# Navigate to backend
cd "E:\MOHAMMAD AHMAD\Courses\Governor Sindh IT\Q4\Hackathon_02\Phase_III_Todo_AI_Chatbot\src\backend"

# Create .env file
copy .env.example .env

# Edit .env and add:
# - DATABASE_URL (already there from Phase-II)
# - BETTER_AUTH_SECRET (already there)
# - COHERE_API_KEY=your_actual_key_here  ← ADD THIS
```

**.env file should look like:**
```env
DATABASE_URL=postgresql://user:pass@host.neon.tech/dbname
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
COHERE_API_KEY=your-cohere-api-key-here
LOG_LEVEL=INFO
```

### Step 2: Install Backend Dependencies

```bash
# Activate virtual environment
venv\Scripts\activate

# Install/verify dependencies
pip install -r requirements.txt
```

### Step 3: Run Database Migration

```bash
# Connect to your Neon database and run:
# psql "your-database-url"

# Or use pgAdmin/other tool to run:
\i migrations/001_create_conversations.sql
```

**Verify tables created:**
```sql
-- Should return 2 rows
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name IN ('conversations', 'messages');
```

### Step 4: Start Backend Server

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Step 5: Frontend Configuration

```bash
# Navigate to frontend (new terminal)
cd "E:\MOHAMMAD AHMAD\Courses\Governor Sindh IT\Q4\Hackathon_02\Phase_III_Todo_AI_Chatbot\src\frontend"

# Verify .env.local exists
# Should contain:
# NEXT_PUBLIC_API_URL=http://localhost:8000
# BETTER_AUTH_SECRET=v8KCReqLlcnLtUifhD4kFdvwCjjssOSk
```

### Step 6: Start Frontend Server

```bash
npm run dev
```

**Expected output:**
```
ready - started server on 0.0.0.0:3000
```

---

## 🎯 Testing the Chatbot

### 1. Open the Application

Navigate to: http://localhost:3000

### 2. Authenticate

- **New user?** Click "Let's Get Started" → Create account
- **Existing user?** Click "Sign in" → Login

### 3. Open Chatbot

- Look for **blue floating button** in bottom-right corner
- Click to open chatbot popup

### 4. Test User Story 1: Create Tasks

Try these commands:
```
Add buy groceries to my list
Create task: Call mom tonight
I need to finish the project report
```

**Expected:** Chatbot confirms task creation with friendly message

### 5. Test User Story 2: View Tasks

Try these commands:
```
Show me all my tasks
What do I need to do?
List my pending tasks
```

**Expected:** Chatbot displays your tasks with titles and status

### 6. Test User Story 3: Complete Tasks

Try these commands:
```
Mark the first task as complete
I finished buy groceries
Complete task [task-id]
```

**Expected:** Task marked as complete with confirmation

### 7. Test User Story 4: Update Tasks

Try these commands:
```
Change buy groceries to buy milk and eggs
Update the first task to call dad
```

**Expected:** Task title updated with confirmation

### 8. Test User Story 5: Delete Tasks

Try these commands:
```
Delete the meeting task
Remove task [task-id]
```

**Expected:** Task deleted with confirmation

### 9. Test User Story 6: Conversation History

1. Have a conversation (send 2-3 messages)
2. Close chatbot (click X)
3. Navigate to different page
4. Reopen chatbot

**Expected:** Previous messages visible, context maintained

---

## 🧪 Manual Test Scenarios

### Scenario 1: First-Time User ✅
1. Create new account
2. Open chatbot
3. See welcome message with examples
4. Type "Add buy milk"
5. Verify task created in database
6. Type "Show my tasks"
7. Verify task listed

### Scenario 2: Conversation Continuity ✅
1. Open chatbot
2. Type "Add task 1"
3. Type "Add task 2"
4. Close chatbot
5. Reopen chatbot
6. Verify both messages visible
7. Type "Show my tasks"
8. Verify both tasks listed

### Scenario 3: Error Handling ✅
1. Send empty message (should be disabled)
2. Send very long message (should work)
3. Send nonsense "asdfghjkl" (should get helpful response)
4. Reference non-existent task (should get error message)

### Scenario 4: User Isolation ✅
1. Login as User A
2. Create tasks via chatbot
3. Logout
4. Login as User B
5. Open chatbot
6. Type "Show my tasks"
7. Verify User B sees ONLY their tasks

---

## 🔍 Backend API Testing

### Test Health Endpoint

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

### Test Chat Endpoint (Manual)

```bash
# 1. Login to get JWT token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Copy the access_token from response

# 2. Test chat
curl -X POST http://localhost:8000/api/YOUR_USER_ID/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"message":"Add buy groceries to my list"}'
```

**Expected Response:**
```json
{
  "conversation_id": "uuid-here",
  "response": "Great! I've added 'Buy groceries' to your todo list.",
  "timestamp": "2026-02-17T...",
  "intent": "create_task",
  "confidence": 0.95
}
```

---

## 🐛 Troubleshooting

### Error: "COHERE_API_KEY not found"

**Problem:** Missing or invalid Cohere API key

**Solution:**
```bash
# Check .env file
cat src/backend/.env

# Should have: COHERE_API_KEY=your_actual_key
# Not: COHERE_API_KEY=your-cohere-api-key-here

# Get real key from: https://dashboard.cohere.com/api-keys
```

### Error: "relation 'conversations' does not exist"

**Problem:** Database migration not run

**Solution:**
```bash
# Connect to Neon database
psql "your-database-url"

# Run migration
\i migrations/001_create_conversations.sql

# Or verify manually:
SELECT * FROM conversations LIMIT 1;
```

### Error: "Failed to send message"

**Problem:** Backend not running or CORS issue

**Solution:**
1. Verify backend running on http://localhost:8000
2. Check browser console for errors
3. Verify NEXT_PUBLIC_API_URL in frontend .env.local
4. Check CORS origins in backend main.py

### Chatbot Not Appearing

**Problem:** User not authenticated or component not loaded

**Solution:**
1. Verify user is logged in (check dashboard)
2. Check browser console for React errors
3. Verify ChatbotPopup imported in dashboard/page.tsx
4. Clear browser cache and reload

### Messages Not Persisting

**Problem:** Database connection issue

**Solution:**
```bash
# Check DATABASE_URL in .env
# Verify connection:
python verify_tables.py

# Should show conversations and messages tables
```

---

## 📊 Success Criteria Checklist

Use this to verify Phase-III is working:

- [ ] Backend server starts without errors
- [ ] Frontend server starts without errors
- [ ] Floating button appears (bottom-right)
- [ ] Chatbot opens on click
- [ ] Welcome message shows examples
- [ ] Can create tasks via chat
- [ ] Can view tasks via chat
- [ ] Can complete tasks via chat
- [ ] Can update tasks via chat
- [ ] Can delete tasks via chat
- [ ] Conversation history persists
- [ ] User isolation enforced
- [ ] Error messages are user-friendly
- [ ] Loading animations work
- [ ] Auto-scroll to latest messages

**All checked?** 🎉 Phase-III is fully functional!

---

## 🎨 UI Tour

### Chatbot States

**Closed:**
- Blue floating button (bottom-right)
- Pulsing animation to attract attention

**Opening:**
- Smooth slide-up animation
- Header with AI Assistant title

**Empty State:**
- Welcome message
- 3 example commands
- Clean, inviting design

**Active Chat:**
- User messages (right, gradient blue)
- Assistant messages (left, white)
- Timestamps on all messages
- Loading animation during API calls

**Input:**
- Text area (auto-resize)
- Send button (gradient blue)
- Disabled state during loading

---

## 📝 Additional Resources

- **Full Documentation:** `PHASE_III_IMPLEMENTATION_COMPLETE.md`
- **API Spec:** `specs/007-ai-chatbot-integration/spec.md`
- **Migration:** `src/backend/migrations/001_create_conversations.sql`
- **Architecture:** See architecture diagram in main documentation

---

## 🚀 Ready for Production?

Before deploying:

1. **Set production COHERE_API_KEY**
2. **Update CORS origins** in backend main.py
3. **Set production URLs** in environment variables
4. **Enable rate limiting** on chat endpoint
5. **Add monitoring** for API errors
6. **Test with real users**

**Deployment guides:** See Phase-IV documentation for Kubernetes deployment.

---

**Happy Chatting! 💬**
