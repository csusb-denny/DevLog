#routes/projects.py - FASTAPI endpoint definitions for Project operations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import SessionLocal

router = APIRouter(prefix="/projects", tags=["Projects"])
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#Create a new Project POST /projects
#Assigned to user with id=1 for simplicity
@router.post("/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db, project, user_id=1)  # temp: assign to user 1
#List all Projects GET /projects
@router.get("/", response_model=list[schemas.Project])
def list_projects(db: Session = Depends(get_db)):
    return crud.get_projects(db)
