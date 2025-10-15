from fastapi import APIRouter
from app.api import integration_types, integrations, workflows, import_export

api_router = APIRouter()

api_router.include_router(integration_types.router)
api_router.include_router(integrations.router)
api_router.include_router(workflows.router)
api_router.include_router(import_export.router)