from fastapi import APIRouter
from app.api import integration_types, integrations, workflows

api_router = APIRouter()

api_router.include_router(integration_types.router)
api_router.include_router(integrations.router)
api_router.include_router(workflows.router)
