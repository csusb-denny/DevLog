# DevLog DevLog — Developer Project Tracker

DevLog is a full-stack developer project tracker built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Alembic**.  
It allows you to create, list, and manage personal or team projects — with JWT authentication, structured migrations, and a REST API ready for frontend integration.

# Tech Stack

**FastAPI - Backend Framework
**PostgreSQL - Database
**Alembic - Schema migrations
**JWT + Passlib - authentication
\*\*Docker Compose - dev environment

## Getting Started

###1. Clone Repo

```bash
git clone https://github.com/csusb-denny/DevLog
cd DevLog

docker compose up --build -d
    backlend: localhost:8000
    Docs: localhost:8000/docs
```

### Run Database Migrations

```
  docker exec devlog_backend alembic upgrade head
```

#Project Structure
DevLog/
├── backend/
│ ├── app/
│ │ ├── routes/
│ │ ├── models.py
│ │ ├── schemas.py
│ │ ├── auth.py
│ │ ├── main.py
│ │ └── seed.py
│ ├── alembic/
│ ├── alembic.ini
│ ├── Dockerfile
│ └── requirements.txt
├── docker-compose.yml
└── README.md
