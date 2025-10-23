#main.py - Entry point for the FastAPI application
from fastapi import FastAPI
from .database import Base, engine
from .routes import users, projects
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request
#Initialize FastAPI app
app = FastAPI(title="DevLog API")
#Create all tables in the database during startup (based on model.py definitions)
Base.metadata.create_all(bind=engine)
#Includes API route modules
app.include_router(users.router)
app.include_router(projects.router)
#Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # narrow in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#Custom 404 Error Handler
@app.exception_handler(404)
async def not_found(_, __):
    return JSONResponse({"detail": "Not Found"}, status_code=404)
#Simple Health Check Endpoint
@app.get("/")
def root():
    return {"message": "DevLog API running!"}
