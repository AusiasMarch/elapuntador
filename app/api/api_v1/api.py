from fastapi import APIRouter

from api.api_v1.endpoints import (
    apuntar,
    dash,
    location,
    login,
    users,
    utils,
)

api_router = APIRouter()


# DRIBIA
api_router.include_router(apuntar.router, prefix="/apuntar", tags=["apuntar"])
api_router.include_router(location.router, prefix="/location", tags=["location"])
api_router.include_router(dash.router, prefix="/dash", tags=["dash"])

api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
