
from pymongo import AsyncMongoClient
from app.config import settings


async def connect_to_database(app):
    client = AsyncMongoClient(settings.mongodb_url)

    # Check database connectivity
    await client.admin.command("ping")

    app.state.mongo_client = client
    app.state.database = client[settings.database_name]

    # Create an index for project lookup
    await app.state.database.projects.create_index(
        "project_name"
    )


async def close_database_connection(app):
    client = getattr(app.state, "mongo_client", None)

    if client is not None:
        await client.close()
