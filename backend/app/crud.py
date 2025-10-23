#Database interaction function(Create, Read, Update, Delete)
from sqlalchemy.orm import Session
from . import models, schemas

# ---- USERS ----
def create_user(db: Session, user: schemas.UserCreate):
    new_user = models.User(username=user.username, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_users(db: Session):
    return db.query(models.User).all()

# ---- PROJECTS ----
def create_project(db: Session, project: schemas.ProjectCreate, user_id: int):
    new_project = models.Project(**project.dict(), owner_id=user_id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

def get_projects(db: Session):
    return db.query(models.Project).all()

from passlib.context import CryptContext
pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# ---- USERS with Password Hashing ----
def create_user(db: Session, user: schemas.UserCreate):
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=pwd.hash(user.password)   # hash it!
    )
    db.add(new_user); db.commit(); db.refresh(new_user)
    return new_user
