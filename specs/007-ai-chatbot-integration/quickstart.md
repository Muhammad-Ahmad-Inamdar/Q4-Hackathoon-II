# Quickstart Guide: Phase-III Todo AI Chatbot Integration

**Feature**: 007-ai-chatbot-integration
**Date**: 2026-02-08
**Audience**: Developers setting up the chatbot feature

## Overview

This guide walks you through setting up the AI chatbot feature from scratch, including database setup, backend configuration, MCP server, and frontend integration.

**Estimated Setup Time**: 30-45 minutes

---

## Prerequisites

- Node.js 18+ and npm/yarn installed
- Python 3.11+ installed
- PostgreSQL database access (Neon Serverless)
- Cohere API account and API key
- Better Auth configured in existing project
- Git repository cloned locally

---

## Step 1: Environment Configuration

### Backend Environment Variables

Create or update `.env` file in the backend directory:

```bash
# Database
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# Cohere API
COHERE_API_KEY=your_cohere_api_key_here

# Better Auth
JWT_SECRET=your_jwt_secret_here
JWT_ALGORITHM=HS256

# Server
PORT=8000
ENVIRONMENT=development

# Logging
LOG_LEVEL=INFO
```

**How to get Cohere API Key**:
1. Sign up at https://cohere.com/
2. Navigate to API Keys section
3. Create a new API key
4. Copy and paste into `.env`

### Frontend Environment Variables

Create or update `.env.local` file in the frontend directory:

```bash
# API Endpoint
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth
NEXT_PUBLIC_AUTH_URL=http://localhost:3000
```

---

## Step 2: Database Migration

### Execute Migration

```bash
# Navigate to backend directory
cd backend

# Run migration script
psql $DATABASE_URL -f ../database/migrations/007_add_conversation_tables.sql
```

**Expected Output**:
```
BEGIN
CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE INDEX
CREATE FUNCTION
CREATE TRIGGER
COMMIT
```

### Verify Migration

```bash
# Connect to database
psql $DATABASE_URL

# Check tables exist
\dt conversations
\dt messages

# Check indexes
\di idx_conversations_user_id
\di idx_messages_conversation_created

# Exit
\q
```

### Rollback (if needed)

```bash
psql $DATABASE_URL -f ../database/migrations/007_rollback_conversation_tables.sql
```

---

## Step 3: Install Dependencies

### Backend Dependencies

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Or using poetry
poetry install
```

**Key Dependencies**:
- `fastapi>=0.104.0`
- `uvicorn[standard]>=0.24.0`
- `sqlmodel>=0.0.14`
- `cohere>=4.0.0`
- `openai-agents-sdk>=1.0.0`
- `python-jose[cryptography]>=3.3.0`
- `psycopg2-binary>=2.9.9`
- `pydantic>=2.0.0`

### Frontend Dependencies

```bash
cd frontend

# Install Node dependencies
npm install
# or
yarn install
```

**Key Dependencies**:
- `next>=14.0.0`
- `react>=18.0.0`
- `tailwindcss>=3.0.0`
- `@better-auth/client`

---

## Step 4: Start Backend Server

### Development Mode

```bash
cd backend

# Start FastAPI server with hot reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Verify Backend

Open browser and navigate to:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

---

## Step 5: Start Frontend Server

### Development Mode

```bash
cd frontend

# Start Next.js development server
npm run dev
# or
yarn dev
```

**Expected Output**:
```
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
event - compiled client and server successfully
```

### Verify Frontend

Open browser and navigate to:
- Home: http://localhost:3000
- Dashboard: http://localhost:3000/dashboard

---

## Step 6: Test the Chatbot

### Manual Testing Scenarios

#### Test 1: Create Task
1. Navigate to Dashboard page
2. Click floating chat button (bottom-right corner)
3. Type: "Add buy groceries to my list"
4. Verify: Task is created and confirmation message appears

#### Test 2: List Tasks
1. In chatbot, type: "Show me all my tasks"
2. Verify: All tasks are displayed with status

#### Test 3: Complete Task
1. In chatbot, type: "Mark buy groceries as complete"
2. Verify: Task is marked complete and confirmation appears

#### Test 4: Conversation History
1. Close chatbot pop-up
2. Refresh page
3. Reopen chatbot
4. Verify: Previous messages are displayed

#### Test 5: Error Handling
1. In chatbot, type: "Complete task 999"
2. Verify: Friendly error message appears (not technical error)

---

## Step 7: Run Tests

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_chat_api.py -v
```

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test
# or
yarn test

# Run with coverage
npm test -- --coverage
```

---

## Troubleshooting

### Issue: Database Connection Failed

**Symptoms**: `psycopg2.OperationalError: could not connect to server`

**Solutions**:
1. Verify DATABASE_URL is correct
2. Check database is running and accessible
3. Verify SSL mode is set correctly for Neon
4. Test connection: `psql $DATABASE_URL`

### Issue: Cohere API Error

**Symptoms**: `CohereAPIError: invalid_api_key`

**Solutions**:
1. Verify COHERE_API_KEY is set in `.env`
2. Check API key is valid at https://cohere.com/
3. Verify API key has not expired
4. Check rate limits are not exceeded

### Issue: JWT Validation Failed

**Symptoms**: `401 Unauthorized` when calling chat endpoint

**Solutions**:
1. Verify JWT_SECRET matches Better Auth configuration
2. Check token is being sent in Authorization header
3. Verify token has not expired
4. Test token decoding: `jwt.decode(token, JWT_SECRET)`

### Issue: Chatbot Pop-up Not Visible

**Symptoms**: Floating button or pop-up doesn't appear

**Solutions**:
1. Check browser console for JavaScript errors
2. Verify ChatbotPopup component is imported in page
3. Check z-index conflicts with existing UI
4. Clear browser cache and reload

### Issue: Messages Not Persisting

**Symptoms**: Conversation history is lost after refresh

**Solutions**:
1. Verify database migration was successful
2. Check conversation_id is being returned and stored
3. Verify messages are being saved to database
4. Check database logs for errors

---

## Development Workflow

### Making Changes

1. **Backend Changes**:
   - Edit files in `backend/src/`
   - Server auto-reloads (if using `--reload`)
   - Test changes at http://localhost:8000/docs

2. **Frontend Changes**:
   - Edit files in `frontend/src/`
   - Next.js auto-reloads
   - Test changes at http://localhost:3000

3. **Database Changes**:
   - Create new migration file
   - Test migration on development database
   - Create rollback script
   - Document changes in data-model.md

### Code Quality Checks

```bash
# Backend linting
cd backend
flake8 src/
black src/ --check
mypy src/

# Frontend linting
cd frontend
npm run lint
npm run type-check
```

---

## Production Deployment

### Backend (Vercel Serverless)

1. Configure environment variables in Vercel dashboard
2. Deploy: `vercel --prod`
3. Verify deployment at production URL
4. Test chat endpoint with production database

### Frontend (Vercel)

1. Configure environment variables in Vercel dashboard
2. Deploy: `vercel --prod`
3. Verify chatbot appears on Dashboard and Home pages
4. Test end-to-end flow in production

### Database (Neon)

1. Run migration on production database
2. Verify tables and indexes created
3. Monitor query performance
4. Set up connection pooling if needed

---

## Monitoring and Logging

### Backend Logs

```bash
# View logs in development
tail -f logs/app.log

# View logs in production (Vercel)
vercel logs <deployment-url>
```

### Database Monitoring

```bash
# Check active connections
SELECT count(*) FROM pg_stat_activity;

# Check slow queries
SELECT query, mean_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### Frontend Monitoring

- Check browser console for errors
- Monitor network requests in DevTools
- Use Vercel Analytics for production monitoring

---

## Performance Optimization

### Backend
- Enable database connection pooling (10-20 connections)
- Implement query result caching if needed
- Monitor Cohere API response times
- Optimize conversation history queries

### Frontend
- Lazy load chatbot component
- Implement message virtualization for long conversations
- Optimize bundle size with code splitting
- Use React.memo for message components

### Database
- Verify indexes are being used (EXPLAIN ANALYZE)
- Monitor query performance
- Consider read replicas for high load
- Implement query timeout limits

---

## Security Checklist

- [ ] JWT_SECRET is strong and not committed to git
- [ ] COHERE_API_KEY is stored securely in environment variables
- [ ] Database credentials are not exposed
- [ ] CORS is configured correctly
- [ ] Rate limiting is enabled on chat endpoint
- [ ] User input is sanitized
- [ ] Error messages don't expose internal details
- [ ] HTTPS is enforced in production
- [ ] Database connections use SSL
- [ ] Logs don't contain sensitive data

---

## Next Steps

1. ✅ Setup complete - chatbot is running locally
2. → Run `/sp.tasks` to generate implementation tasks
3. → Begin implementation following task order
4. → Test each user story as implemented
5. → Deploy to production when all tests pass

---

## Support and Resources

- **Cohere Documentation**: https://docs.cohere.com/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Next.js Documentation**: https://nextjs.org/docs
- **MCP SDK**: https://github.com/modelcontextprotocol/sdk
- **Better Auth**: https://better-auth.com/docs

---

## Appendix: Useful Commands

```bash
# Database
psql $DATABASE_URL                          # Connect to database
psql $DATABASE_URL -c "SELECT * FROM conversations LIMIT 5;"  # Query

# Backend
uvicorn src.main:app --reload              # Start server
pytest -v                                   # Run tests
black src/                                  # Format code

# Frontend
npm run dev                                 # Start dev server
npm test                                    # Run tests
npm run build                               # Build for production

# Git
git status                                  # Check status
git add .                                   # Stage changes
git commit -m "message"                     # Commit
git push origin 007-ai-chatbot-integration  # Push to branch
```
