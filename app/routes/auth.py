from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import User
from app.services.auth_service import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ── SCHEMAS ──
class RegisterInput(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    email: str


# ── DEPENDENCY: get current user from JWT ──
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user


# ── REGISTER ──
@router.post(
    "/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED
)
def register(data: RegisterInput, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user = User(email=data.email, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    token = create_access_token({"sub": user.email})
    return TokenResponse(access_token=token, token_type="bearer", email=user.email)


# ── LOGIN ──
@router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    token = create_access_token({"sub": user.email})
    return TokenResponse(access_token=token, token_type="bearer", email=user.email)


# ── ME ──
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at.isoformat(),
    }
