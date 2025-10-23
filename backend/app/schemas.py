#schemas.py Pydantic models for request and response validation
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime
#Base Schema for Project Definitions
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
#Schema for creating new Project
class ProjectCreate(ProjectBase):
    pass
#Schema for Project with additional fields
class Project(ProjectBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
#Base Schema for User Definitions
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