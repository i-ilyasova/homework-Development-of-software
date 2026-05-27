from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

import crud
from database import get_db
from models import User
from schemas import LoginRequest, TokenResponse, UserCreate, UserResponse
from security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    is_revoked,
    revoke_token,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])
_bearer = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_token(credentials.credentials)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    if is_revoked(payload["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
        )
    user = db.get(User, int(payload["sub"]))
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    return user


def require_write(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role == "readonly":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Read-only access: operation not permitted",
        )
    return current_user


@router.post("/register", response_model=UserResponse, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, data.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    return crud.create_user(db, data.username, data.email, hash_password(data.password), data.role)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, data.username)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive",
        )
    return TokenResponse(
        access_token=create_access_token(user.id, user.role),
        refresh_token=create_refresh_token(user.id),
    )


@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    current_user: User = Depends(get_current_user),
):
    payload = decode_token(credentials.credentials)
    revoke_token(payload["jti"])
    return {"detail": "Successfully logged out"}


@router.post("/refresh", response_model=TokenResponse)
def refresh_tokens(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    db: Session = Depends(get_db),
):
    payload = decode_token(credentials.credentials)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    if is_revoked(payload["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has been revoked",
        )
    revoke_token(payload["jti"])
    user = db.get(User, int(payload["sub"]))
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    return TokenResponse(
        access_token=create_access_token(user.id, user.role),
        refresh_token=create_refresh_token(user.id),
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
