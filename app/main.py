from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from api.api_v1.api import api_router
from core import config
from db.session import Session

app = FastAPI(title=config.PROJECT_NAME, openapi_url="/api/v1/openapi.json")

# CORS Cross-origin resource sharing
origins = []

# Set all CORS enabled origins
if config.BACKEND_CORS_ORIGINS:
    origins_raw = config.BACKEND_CORS_ORIGINS.split(",")
    for origin in origins_raw:
        use_origin = origin.strip()
        origins.append(use_origin)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),

app.include_router(api_router, prefix=config.API_V1_STR)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    print(dir(request))
    # print('request.auth')
    # print(request.auth)
    print('request.body')
    print(request.body)
    print('request.form')
    print(request.form)
    print('request.headers')
    print(request.headers)
    print('request.json')
    print(request.json)
    print('request.session')
    print(request.session)
    print('request.user')
    print(request.user)
    
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response
