from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from api.api_v1.api import api_router
from core import config
from core import jwt
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


from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser, UnauthenticatedUser,
    AuthCredentials
)
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import PlainTextResponse
import base64
import binascii


# class BasicAuthBackend(AuthenticationBackend):
#     async def authenticate(self, request):
#         if "Authorization" not in request.headers:
#             return
#
#         auth = request.headers["Authorization"]
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
    # # print(dir(request))
    # print('request.auth')
    # print(request.auth)
    # print(dir(request.auth))
    # print(request.auth.scopes)
    # # print('request.body')
    # # print(await request.body())
    # print('request.form')
    # print(await request.form())
    # print('request.headers')
    # print(request.headers)
    # print('request.json')
    # print(a)
    # print(dir(a))
    # print(a.keys())
    # print(a['originalDetectIntentRequest'])
    # print(a['originalDetectIntentRequest']['payload'])
    # print(a['originalDetectIntentRequest']['payload']['user'])
    # print(a['originalDetectIntentRequest']['payload']['user']['idToken'])
    a = await request.json()
    print(a['originalDetectIntentRequest']['payload']['user']['idToken'])
    print(type(a['originalDetectIntentRequest']['payload']['user']['idToken']))
    print(jwt.decode_google_token(a['originalDetectIntentRequest']['payload']['user']['idToken']))
    
    # # print('request.session')  # "SessionMiddleware must be installed to access request.session"
    # # print(request.session)
    # print('request.user')
    # print(request.user)
    # print(dir(request.user))
    # print(request.user.display_name)
    # # print(request.user.identity)
    # print(request.user.is_authenticated)
    
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response


# app = AuthenticationMiddleware(app, backend=BasicAuthBackend())