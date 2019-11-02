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


# from starlette.authentication import (
#     AuthenticationBackend, AuthenticationError, SimpleUser, UnauthenticatedUser,
#     AuthCredentials
# )
# from starlette.middleware.authentication import AuthenticationMiddleware
# from starlette.responses import PlainTextResponse
# import base64
# import binascii
#
#
# class BasicAuthBackend(AuthenticationBackend):
#     async def authenticate(self, request):
#         if "idToken" not in request.headers:
#             return
#
#         id_token = request.json()['originalDetectIntentRequest']['payload']['user']['idToken']
#
#         auth = jwt.decode_google_token(id_token)
#         try:
#             scheme, credentials = auth.split()
#             if scheme.lower() != 'basic':
#                 return
#             decoded = base64.b64decode(credentials).decode("ascii")
#         except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
#             raise AuthenticationError('Invalid basic auth credentials')
#
#         username, _, password = decoded.partition(":")
#         # TODO: You'd want to verify the username and password here,
#         #       possibly by installing `DatabaseMiddleware`
#         #       and retrieving user information from `request.database`.
#         return AuthCredentials(["authenticated"]), SimpleUser(username)



@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response

# app = AuthenticationMiddleware(app, backend=BasicAuthBackend())