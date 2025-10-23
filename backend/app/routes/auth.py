from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..auth import authenticate, create_access_token, get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate(db, form.username, form.password)
    if not user:
        raise HTTPException(401, "Incorrect username or password")
    return {"access_token": create_access_token(user.username), "token_type": "bearer"}
