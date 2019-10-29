import os
from environs import Env

env = Env()
env_files = [x for x in os.listdir('.') if x.endswith('.env')]
for env_file in env_files:
    env.read_env(env_file, recurse=False)


def get_env_variable(var_name):
    variable = os.getenv(var_name)
    if variable is not None:
        return variable
    else:
        try:
            return env(var_name)
        except:
            return None

def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = get_env_variable(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


API_V1_STR = "/api/v1"

SECRET_KEY = os.getenvb(b"SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = os.urandom(32)

SERVER_NAME = get_env_variable("SERVER_NAME")
SERVER_HOST = get_env_variable("SERVER_HOST")
PROJECT_NAME = get_env_variable("PROJECT_NAME")
SENTRY_DSN = get_env_variable("SENTRY_DSN")

POSTGRES_SERVER = get_env_variable("POSTGRES_SERVER")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PASSWORD = get_env_variable("POSTGRES_PASSWORD")
POSTGRES_DB = get_env_variable("POSTGRES_DB")
SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
)

FIRST_SUPERUSER = get_env_variable("FIRST_SUPERUSER")
FIRST_SUPERUSER_PASSWORD = get_env_variable("FIRST_SUPERUSER_PASSWORD")

USERS_OPEN_REGISTRATION = getenv_boolean("USERS_OPEN_REGISTRATION")
