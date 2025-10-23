#Dockerfile for FastAPI backend application

# 1. Use python base image
# 2. Set working directory
# 3. Copy requirements file and install dependencies
# 4. Install python dependencies
# 5. Copy application code
# 6. Command to run the application
# This runs the FastAPI app using Uvicorn
# --host 0.0.0.0   makes it accessible from outside container
# --port 8000      standard app port
# --reload         enables hot reload in dev mode
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]



FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

