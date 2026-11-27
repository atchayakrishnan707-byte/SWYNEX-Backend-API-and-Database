
# SWYNEX Backend API and Database

## ScopeSentry

AI-Powered Project Scope Management and Change Intelligence Platform.

## Overview

This repository contains the backend API and database implementation for ScopeSentry.

The backend manages project information, validates incoming requests and stores project records in MongoDB.

## Technology Stack

- Python
- FastAPI
- MongoDB
- PyMongo Async
- Pydantic
- Uvicorn

## Features

- Create projects
- Retrieve all projects
- Retrieve individual projects
- Update project details
- Delete projects
- Request validation
- MongoDB persistence
- Error handling
- API documentation through Swagger UI

## Project Structure

```text
SWYNEX-Backend-API-and-Database/
│
├── app/
│   ├── routes/
│   │   ├── __init__.py
│   │   └── projects.py
│   │
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   └── models.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation


git clone https://github.com/atchayakrishnan707-byte/SWYNEX-Backend-API-and-Database.git

cd SWYNEX-Backend-API-and-Database

python -m venv .venv

.venv\Scripts\Activate.ps1

pip install -r requirements.txt

copy .env.example .env

python -m uvicorn app.main:app --reload


## API Documentation

Open:

http://127.0.0.1:8000/docs

## Base API URL

http://127.0.0.1:8000/api

## Project Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/projects/ | Create project |
| GET | /api/projects/ | Get all projects |
| GET | /api/projects/{id} | Get project |
| PUT | /api/projects/{id} | Update project |
| DELETE | /api/projects/{id} | Delete project |

## Validation

The project resource validates:

- Project name length
- Description length
- Positive budget
- Currency format
- Valid dates
- Project status
- MongoDB ObjectId format

## Project Status

Initial backend API and MongoDB persistence implementation for the SWYNEX Full Stack Developer Internship.

Additional modules such as authentication, requirement management, AI analysis and approval workflows are planned for subsequent development.

