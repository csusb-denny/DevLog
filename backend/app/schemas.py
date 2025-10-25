# app/schemas.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

# ------------------------
# USER SCHEMAS
# ------------------------
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# ------------------------
# PROJECT SCHEMAS
# ------------------------
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ProjectOut(ProjectBase):
    id: int
    owner_id: int
    # keep timestamps optional unless your DB has them
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

# ------------------------
# LOG SCHEMAS (if you expose logs)
# ------------------------
class LogBase(BaseModel):
    message: str

class LogCreate(LogBase):
    project_id: int

class LogOut(LogBase):
    id: int
    project_id: int
    model_config = ConfigDict(from_attributes=True)
