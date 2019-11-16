from fastapi import APIRouter

from api.api_v1.endpoints import (
    apuntar,
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
api_router.include_router(apuntar.router, prefix="/apuntar", tags=["apuntar"])
api_router.include_router(dash.router, prefix="/dash", tags=["dash"])
