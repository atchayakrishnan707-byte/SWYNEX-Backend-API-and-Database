
from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pymongo.errors import PyMongoError

from app.models import ProjectCreate, ProjectUpdate


router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"]
)


def get_database(request: Request):
    return request.app.state.database


def serialize_project(project):
    project["id"] = str(project.pop("_id"))
    return project


def validate_project_id(project_id: str):
    if not ObjectId.is_valid(project_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid project ID"
        )

    return ObjectId(project_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
async def create_project(
    project: ProjectCreate,
    db=Depends(get_database)
):
    project_data = project.model_dump()

    project_data["created_at"] = datetime.now(timezone.utc)
    project_data["updated_at"] = datetime.now(timezone.utc)

    try:
        result = await db.projects.insert_one(project_data)

        created_project = await db.projects.find_one(
            {"_id": result.inserted_id}
        )

        return serialize_project(created_project)

    except PyMongoError:
        raise HTTPException(
            status_code=500,
            detail="Could not save project"
        )


@router.get("/")
async def get_all_projects(
    db=Depends(get_database)
):
    try:
        projects = await db.projects.find().to_list(
            length=100
        )

        return [
            serialize_project(project)
            for project in projects
        ]

    except PyMongoError:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve projects"
        )


@router.get("/{project_id}")
async def get_project(
    project_id: str,
    db=Depends(get_database)
):
    object_id = validate_project_id(project_id)

    project = await db.projects.find_one(
        {"_id": object_id}
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return serialize_project(project)


@router.put("/{project_id}")
async def update_project(
    project_id: str,
    project: ProjectUpdate,
    db=Depends(get_database)
):
    object_id = validate_project_id(project_id)

    update_data = project.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Provide at least one field to update"
        )

    update_data["updated_at"] = datetime.now(timezone.utc)

    existing = await db.projects.find_one(
        {"_id": object_id}
    )

    if existing is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    # Validate dates against existing values too
    new_start = update_data.get(
        "start_date", existing["start_date"]
    )
    new_end = update_data.get(
        "end_date", existing["end_date"]
    )

    if new_end < new_start:
        raise HTTPException(
            status_code=422,
            detail="End date cannot be earlier than start date"
        )

    await db.projects.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    updated_project = await db.projects.find_one(
        {"_id": object_id}
    )

    return serialize_project(updated_project)


@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    db=Depends(get_database)
):
    object_id = validate_project_id(project_id)

    result = await db.projects.delete_one(
        {"_id": object_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return {
        "message": "Project deleted successfully",
        "project_id": project_id
    }
