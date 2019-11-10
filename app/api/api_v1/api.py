from fastapi import APIRouter

from api.api_v1.endpoints import (
    apuntes,
    dash,
    login,
    users,
    utils,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# DRIBIA
api_router.include_router(apuntes.router, prefix="/apuntes", tags=["apuntes", "peso", "altura"])
api_router.include_router(dash.router, prefix="/dash", tags=["dash"])
