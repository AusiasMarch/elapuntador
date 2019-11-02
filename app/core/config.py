import os
from environs import Env

env = Env()
print(os.listdir('.'))
env_files = [x for x in os.listdir('.') if x.endswith('.env')]
env_files = [x for x in env_files if '_{}'.format(x) not in env_files]
for env_file in env_files:
    print("Loading {} file.".format(env_file))
    env.read_env(env_file, recurse=False)


def get_env_variable(var_name):
    print(var_name)
    variable = os.getenv(var_name)
    print(variable)
    if variable is not None:
        return variable
    else:
        try:
            print(env(var_name))
            return env(var_name)
        except:
            return None


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = get_env_variable(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


GOOGLE_CLIENTID = get_env_variable("GOOGLE_CLIENTID")
GOOGLE_ISS = get_env_variable("GOOGLE_ISS")

API_V1_STR = get_env_variable("API_V1_STR")

SECRET_KEY = get_env_variable("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = os.urandom(32)

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

SERVER_NAME = get_env_variable("SERVER_NAME")
SERVER_HOST = get_env_variable("SERVER_HOST")
BACKEND_CORS_ORIGINS = get_env_variable(
    "BACKEND_CORS_ORIGINS"
)  # a string of origins separated by commas, e.g: "http://localhost, http://localhost:4200, http://localhost:3000, http://localhost:8080, http://local.dockertoolbox.tiangolo.com"
PROJECT_NAME = get_env_variable("PROJECT_NAME")
SENTRY_DSN = get_env_variable("SENTRY_DSN")

POSTGRES_SERVER = get_env_variable("POSTGRES_SERVER")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PASSWORD = get_env_variable("POSTGRES_PASSWORD")
POSTGRES_DB = get_env_variable("POSTGRES_DB")
SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
)

SMTP_TLS = getenv_boolean("SMTP_TLS", True)
SMTP_PORT = None
_SMTP_PORT = get_env_variable("SMTP_PORT")
if _SMTP_PORT is not None:
    SMTP_PORT = int(_SMTP_PORT)
SMTP_HOST = get_env_variable("SMTP_HOST")
SMTP_USER = get_env_variable("SMTP_USER")
SMTP_PASSWORD = get_env_variable("SMTP_PASSWORD")
EMAILS_FROM_EMAIL = get_env_variable("EMAILS_FROM_EMAIL")
EMAILS_FROM_NAME = PROJECT_NAME
EMAIL_RESET_TOKEN_EXPIRE_HOURS = 48
EMAIL_TEMPLATES_DIR = "/app/app/email-templates/build"
EMAILS_ENABLED = SMTP_HOST and SMTP_PORT and EMAILS_FROM_EMAIL

FIRST_SUPERUSER_MAIL = get_env_variable("FIRST_SUPERUSER_MAIL")
FIRST_SUPERUSER_PASSWORD = get_env_variable("FIRST_SUPERUSER_PASSWORD")
FIRST_SUPERUSER_RELATION = get_env_variable("FIRST_SUPERUSER_RELATION")
FIRST_SUPERUSER_NAME = get_env_variable("FIRST_SUPERUSER_NAME")

USERS_OPEN_REGISTRATION = getenv_boolean("USERS_OPEN_REGISTRATION")
