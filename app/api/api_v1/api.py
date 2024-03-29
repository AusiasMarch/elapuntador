from fastapi import APIRouter

from api.api_v1.endpoints import (
    apuntar,
    card_plots,
    dash,
    location,
    login,
    temperature,
    users,
    utils,
)

api_router = APIRouter()


# DRIBIA
api_router.include_router(apuntar.router, prefix="/apuntar", tags=["apuntar"])
api_router.include_router(card_plots.router, prefix="/card_plots", tags=["apuntar"])
api_router.include_router(location.router, prefix="/location", tags=["location"])
api_router.include_router(temperature.router, prefix="/temperature", tags=["location"])
api_router.include_router(dash.router, prefix="/dash", tags=["dash"])

api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
