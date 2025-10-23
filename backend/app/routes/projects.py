#routes/projects.py - FASTAPI endpoint definitions for Project operations
from fastapi import APIRouter, Depends, HTTPException, Query
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


@router.put("/{project_id}", response_model=schemas.Project)
#Update a Project PUT /projects/{project_id}
def update_project(project_id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    obj = db.query(models.Project).get(project_id)
    if not obj:
        raise HTTPException(404, "Project not found")
    obj.title = project.title
    obj.description = project.description
    db.commit()
    db.refresh(obj)
    return obj
#Delete a Project DELETE /projects/{project_id}
@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Project).get(project_id)
    if not obj:
        raise HTTPException(404, "Project not found")
    db.delete(obj)
    db.commit()
    return
#List Projects with search and pagination GET /projects
@router.get("/", response_model=list[schemas.Project])
def list_projects(
    db: Session = Depends(get_db),
    q: str | None = Query(default=None, description="Search in title/description"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    query = db.query(models.Project)
    if q:
        pattern = f"%{q}%"
        query = query.filter((models.Project.title.ilike(pattern)) | (models.Project.description.ilike(pattern)))
    return query.order_by(models.Project.created_at.desc()).limit(limit).offset(offset).all()
