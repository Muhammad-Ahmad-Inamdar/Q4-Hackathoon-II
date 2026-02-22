"""
Todo App API - FastAPI Backend

This is the main entry point for the FastAPI application.
Run with: python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""

import logging
import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Import routers from app package
from app.auth.router import auth_router
from app.tasks.router import tasks_router
from app.database import create_tables

# Add backend root to path for Phase-III imports (api, services, agents)
backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

# Import Phase-III chat API
from api.chat import chat_router

# Set the same secret key for JWT compatibility with Better Auth
os.environ.setdefault("BETTER_AUTH_SECRET", os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup: Create database tables
    logger.info("Creating database tables...")
    create_tables()
    logger.info("Database tables created successfully")
    
    yield
    
    # Shutdown: cleanup if needed
    logger.info("Shutting down...")


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


# Create tables on startup (moved to lifespan handler)
# create_tables()

app = FastAPI(title="Todo App API", version="1.0.0", lifespan=lifespan)

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://localhost:3002",
    "http://127.0.0.1:3002",
]

logger.info(f"Configuring CORS with origins: {origins}")

# Note: Middleware must be added before routers
# Using middleware stack directly for compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

logger.info("CORS middleware configured successfully")

# Include routers (must be after all middleware)
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks_router, prefix="/api/tasks", tags=["tasks"])
app.include_router(chat_router, prefix="/api", tags=["chat"])

logger.info("Routers included successfully")


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
    logger.info("Starting server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
