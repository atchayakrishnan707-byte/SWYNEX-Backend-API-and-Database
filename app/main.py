
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import (
    connect_to_database,
    close_database_connection
)

from app.routes.projects import router as project_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_database(app)

    yield

    await close_database_connection(app)


app = FastAPI(
    title="ScopeSentry Backend API",
    description="Backend API for AI-powered project scope management",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(project_router)


@app.get("/")
async def home():
    return {
        "application": "ScopeSentry",
        "message": "Welcome to ScopeSentry Backend API",
        "status": "Running"
    }


@app.get("/api/health")
async def health():
    await app.state.database.command("ping")

    return {
        "application": "ScopeSentry",
        "database": "Connected",
        "status": "Healthy"
    }
