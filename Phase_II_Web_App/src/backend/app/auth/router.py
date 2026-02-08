from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from .service import create_user, authenticate_user, create_access_token
from ..database import get_session
from ..models import User, UserRegistration, UserLogin, Token
from typing import Dict
from datetime import datetime

auth_router = APIRouter()


@auth_router.post("/register", response_model=Token)
def register(user_data: UserRegistration, session: Session = Depends(get_session)):
    """Register a new user"""
    # Check if user already exists
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    try:
        user = create_user(session, user_data.email, user_data.password)

        # Create access token
        token_data = {"sub": user.email, "user_id": user.id}
        access_token = create_access_token(data=token_data)

        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@auth_router.post("/login", response_model=Token)
def login(user_data: UserLogin, session: Session = Depends(get_session)):
    """Login user and return access token"""
    user = authenticate_user(session, user_data.email, user_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update last login
    user.last_login_at = datetime.utcnow()
    session.add(user)
    session.commit()

    # Create access token
    token_data = {"sub": user.email, "user_id": user.id}
    access_token = create_access_token(data=token_data)

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/logout")
def logout():
    """Logout user (client-side token removal is sufficient)"""
    return {"message": "Successfully logged out"}


