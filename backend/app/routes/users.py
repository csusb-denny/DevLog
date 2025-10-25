# app/routes/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import SessionLocal
from .. import models, schemas
from ..auth import get_current_user, pwd  # pwd is your CryptContext

router = APIRouter(prefix="/users", tags=["Users"])

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE user (register)
@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    # check unique username/email if you want
    if db.query(models.User).filter(models.User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(
        username=payload.username,
        email=payload.email,
        password=pwd.hash(payload.password),  # hash with the same context used by auth
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# (Optional) LIST all users (admin/debug)
@router.get("/", response_model=List[schemas.UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # You may want to restrict this endpoint. For now it lists all for debugging.
    return db.query(models.User).order_by(models.User.id.asc()).all()

# Current user
@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user
