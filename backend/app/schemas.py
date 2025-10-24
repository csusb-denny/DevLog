#schemas.py Pydantic models for request and response validation
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime
from datetime import date

#Base Schema for Project Definitions
class ProjectBase(BaseModel):
    title: str
    description: str | None = None
#Schema for creating new Project
class ProjectCreate(ProjectBase):
    pass
#Schema for Project with additional fields
class Project(ProjectBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None    

class ProjectOut(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime | None = None   # <- optional
    updated_at: datetime | None = None   # <- optional
    model_config = ConfigDict(from_attributes=True)  # <- Pydantic v2: replaces orm_mode=True
#Base Schema for User Definitionsa
class UserBase(BaseModel):
    username: str
    email: EmailStr
#Schema for creating new User
class UserCreate(UserBase):
    password: str
#Schema for User with additional fields
class User(UserBase):
    id: int
    projects: List[Project] = []
    model_config = ConfigDict(from_attributes=True)

class LogBase(BaseModel):
    project_id: int
    content: str

class LogCreate(LogBase):
    pass

class Log(LogBase):
    id: int
    date: date
    model_config = ConfigDict(from_attributes=True)  # Pydantic v2