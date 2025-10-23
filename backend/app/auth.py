from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User
from passlib.context import CryptContext
import os

SECRET = os.getenv("JWT_SECRET", "change-me")
ALGO = "HS256"
ACCESS_MIN = int(os.getenv("JWT_MINUTES", "60"))
pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def authenticate(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd.verify(password, user.password):
        return None
    return user

def create_access_token(sub: str):
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_MIN)
    return jwt.encode({"sub": sub, "exp": exp}, SECRET, algorithm=ALGO)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        username: str = payload.get("sub")
    except JWTError:
        raise HTTPException(401, "Invalid token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(401, "User not found")
    return user
