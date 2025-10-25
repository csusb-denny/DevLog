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
  #apply migrations (inside backend container)
docker exec -e DATABASE_URL="postgresql+psycopg2://devlog_user:devlog_pass@db:5432/devlog_db" \
  devlog_backend sh -lc "cd /app && alembic upgrade head"

```
####Create User
```
curl -sS -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  --data '{"username":"denny","email":"denny@example.com","password":"pass123"}'

```
#####Get a Token
```
curl -sS -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data "username=denny&password=pass123"
```

######Create and List projects (API)
```
# set TOKEN in your shell before running these:
# TOKEN=<paste_token_here>

curl -sS -X POST http://localhost:8000/projects/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"title":"My First Project","description":"hello world"}'

curl -sS http://localhost:8000/projects/ -H "Authorization: Bearer $TOKEN"

```
######Frontend(local dev)
```
cd devlog-frontend
npm install
npm run dev -- --port 5163
```

#Project Structure
DevLog/
├─ docker-compose.yml
├─ backend Dockerfile (in /app)
├─ app/
│  ├─ main.py               # CORS + routers + docs redirect
│  ├─ database.py           # SessionLocal, engine, Base
│  ├─ models.py             # User, Project, Log (FKs with CASCADE)
│  ├─ schemas.py            # Pydantic v2 (UserOut, ProjectOut, etc.)
│  ├─ auth.py               # pwd CryptContext, /auth/token, get_current_user
│  └─ routes/
│     ├─ users.py           # register, list, /me
│     ├─ projects.py        # full CRUD, user-scoped, search
│     └─ auth.py            # token endpoint
├─ alembic.ini
├─ alembic/                 # env.py, versions/
└─ devlog-frontend/         # Vite React app
