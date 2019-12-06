import os
import shutil
import gzip
import logging
from logging.handlers import RotatingFileHandler


from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from api.api_v1.api import api_router
from core import config
from db.session import Session


class GZipRotator:
    def __call__(self, source, dest):
        os.rename(source, dest)
        f_in = open(dest, 'rb')
        f_out = gzip.open('%s.gz' % dest, 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        os.remove(dest)


# shutil.rmtree('/tmp/elapuntador', ignore_errors=True)
os.makedirs('/tmp/elapuntador', exist_ok=True)

log_folder = config.LOG_DIR
os.makedirs(log_folder, exist_ok=True)
handler = RotatingFileHandler(os.path.join(log_folder, 'elapuntador.log'), maxBytes=100 * 1024 * 1024, backupCount=5)
log = logging.getLogger('elapuntador')
log.rotator = GZipRotator()
log.setLevel(logging.getLevelName(config.LOG_LEVEL))  # CRITICAL, ERROR, WARNING, INFO or DEBUG
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)8s - %(module)s - %(funcName)s - %(message)s"))
log.addHandler(handler)


log.info(f"Starting {config.PROJECT_NAME} server.")
app = FastAPI(title=config.PROJECT_NAME, openapi_url="/api/v1/openapi.json")
log.info(f"{config.PROJECT_NAME} server started.")


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
