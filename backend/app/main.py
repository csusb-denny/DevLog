#main.py - Entry point for the FastAPI application
from fastapi import FastAPI
from .database import Base, engine
from .routes import users, projects
#Initialize FastAPI app
app = FastAPI(title="DevLog API")
#Create all tables in the database during startup (based on model.py definitions)
Base.metadata.create_all(bind=engine)
#Includes API route modules
app.include_router(users.router)
app.include_router(projects.router)
#Simple Health Check Endpoint
@app.get("/")
def root():
    return {"message": "DevLog API running!"}
