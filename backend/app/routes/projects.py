# app/routes/projects.py

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List

from ..database import SessionLocal
from .. import models, schemas
from ..auth import get_current_user  # must return models.User

router = APIRouter(prefix="/projects", tags=["Projects"])


# ---------- DB Session dependency ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- CREATE ----------
@router.post("/", response_model=schemas.ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    obj = models.Project(
        title=project.title,
        description=project.description,
        owner_id=current_user.id,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ---------- READ (List) ----------
@router.get("/", response_model=List[schemas.ProjectOut])
def list_projects(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    q: str | None = Query(default=None, description="Search title/description (case-insensitive)"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    query = db.query(models.Project).filter(models.Project.owner_id == current_user.id)
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                models.Project.title.ilike(like),
                models.Project.description.ilike(like),
            )
        )

    # order by newest first (fallback to id if you don't have timestamps)
    query = query.order_by(models.Project.id.desc())

    return query.offset(offset).limit(limit).all()


# ---------- READ (By ID) ----------
@router.get("/{project_id}", response_model=schemas.ProjectOut)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    obj = (
        db.query(models.Project)
        .filter(models.Project.id == project_id, models.Project.owner_id == current_user.id)
        .first()
    )
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return obj


# ---------- UPDATE (Partial) ----------
@router.patch("/{project_id}", response_model=schemas.ProjectOut)
def update_project(
    project_id: int,
    payload: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    obj = (
        db.query(models.Project)
        .filter(models.Project.id == project_id, models.Project.owner_id == current_user.id)
        .first()
    )
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    # apply only provided fields
    if payload.title is not None:
        obj.title = payload.title
    if payload.description is not None:
        obj.description = payload.description

    db.commit()
    db.refresh(obj)
    return obj


# ---------- UPDATE (Full) ----------
@router.put("/{project_id}", response_model=schemas.ProjectOut)
def replace_project(
    project_id: int,
    payload: schemas.ProjectCreate,  # full shape: title, description
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    obj = (
        db.query(models.Project)
        .filter(models.Project.id == project_id, models.Project.owner_id == current_user.id)
        .first()
    )
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    obj.title = payload.title
    obj.description = payload.description

    db.commit()
    db.refresh(obj)
    return obj


# ---------- DELETE ----------
@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    obj = (
        db.query(models.Project)
        .filter(models.Project.id == project_id, models.Project.owner_id == current_user.id)
        .first()
    )
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    # If your DB has ON DELETE CASCADE for logs, this is unnecessary.
    # Keeping it to be safe in case FK wasn't created with cascade.
    db.query(models.Log).filter(models.Log.project_id == obj.id).delete(synchronize_session=False)

    db.delete(obj)
    db.commit()
    # 204 = no body
    return
