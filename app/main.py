from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.authentication import AuthenticationError
from starlette.requests import Request

from api.api_v1.api import api_router
from core import jwt
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
    request.state.db = Session()
    
    response = await call_next(request)
    request.state.db.close()
    return response

@app.middleware("http")
async def is_google_middleware(request: Request, call_next):
    user_agent = request.headers['user-agent']
    if user_agent == 'Google-Dialogflow':
        body = await request.json()
        id_token = body['originalDetectIntentRequest']['payload']['user']['idToken']
        decoded_token = jwt.decode_google_token(id_token)
        if decoded_token['iss'] != 'https://accounts.google.com' or decoded_token['aud'] != config.GOOGLE_2_MIAPIO_CLIENT_ID:
            raise AuthenticationError('Invalid basic auth credentials')
        request.state.email = decoded_token['email']
        
    response = await call_next(request)
    return response

# app = AuthenticationMiddleware(app, backend=BasicAuthBackend())