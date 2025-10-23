#Database.py - Handles database connection and session management
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
#Reads database URL from environment variable (docker-compose.yml)
DATABASE_URL = os.getenv("DATABASE_URL")
#Creates a session factory - used to interact with the database
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Class for all ORM Models(User, Project, etc....)
Base = declarative_base()
