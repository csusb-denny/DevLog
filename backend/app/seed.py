from .database import SessionLocal
from .models import User, Project
from passlib.context import CryptContext
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()
u = User(username="denny", email="denny@example.com", password=pwd.hash("pass123"))
db.add(u); db.commit(); db.refresh(u)
db.add_all([
    Project(title="Alarm Clock", description="PIC18F46K22 build", owner_id=u.id),
    Project(title="ETL Pipeline", description="Airflow + Postgres", owner_id=u.id),
])
db.commit()
db.close()
print("Seeded.")
