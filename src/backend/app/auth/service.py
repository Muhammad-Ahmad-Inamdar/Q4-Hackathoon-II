from sqlmodel import Session, select
from app.models import User
from datetime import datetime, timedelta
from typing import Optional
import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError
import os


def create_user(session: Session, email: str, password: str) -> User:
    """Create a new user with hashed password"""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user = User(
        email=email,
        password=hashed_password.decode('utf-8'),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password"""
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    if not user:
        return None

    # Verify password
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return user

    return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": expire})

    secret_key = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")

    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return payload"""
    try:
        secret_key = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except InvalidTokenError:
        return None
    except Exception:
        return None
