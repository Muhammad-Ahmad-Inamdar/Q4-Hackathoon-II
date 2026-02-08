import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from .auth.router import auth_router
from .tasks.router import tasks_router
from .database import create_tables
import os

# Set the same secret key for JWT compatibility with Better Auth
os.environ.setdefault("BETTER_AUTH_SECRET", os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

# Create tables on startup
create_tables()

app = FastAPI(title="Todo App API", version="1.0.0")

# ✅ STEP 1: CORS FIRST (before any other middleware)
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
origins = [
    frontend_url,
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# ✅ STEP 2: Security headers AFTER CORS
app.add_middleware(SecurityHeadersMiddleware)

# ✅ STEP 3: Include routers
# Router has /register, so prefix="/api/auth" creates /api/auth/register ✅
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks_router, prefix="/api/tasks", tags=["tasks"])

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Todo App API is running!"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "cors_enabled": True,
        "allowed_origins": origins
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)