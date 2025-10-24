from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import SessionLocal

router = APIRouter(prefix="/logs", tags=["Logs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Log)
def create_log(log: schemas.LogCreate, db: Session = Depends(get_db)):
    proj = db.query(models.Project).get(log.project_id)
    if not proj:
        raise HTTPException(404, "Project not found")
    obj = models.Log(project_id=log.project_id, content=log.content)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/", response_model=list[schemas.Log])
def list_logs(project_id: int | None = Query(default=None), db: Session = Depends(get_db)):
    q = db.query(models.Log)
    if project_id is not None:
        q = q.filter(models.Log.project_id == project_id)
    return q.order_by(models.Log.date.desc(), models.Log.id.desc()).all()
