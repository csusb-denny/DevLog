#models.py - SQL Alchemy models for Users and Projects that define database structure
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base
#User table model
class User(Base):
    __tablename__ = "users" #actual table name
    #columns 
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    #relationship to projects
    projects = relationship("Project", back_populates="owner")
#project table model
class Project(Base):
    __tablename__ = "projects" #actual table name
    #columns
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    #foreign key to link to user
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="projects")
