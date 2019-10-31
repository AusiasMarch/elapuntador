import requests

import crud
from core import config
from db.session import db_session
from models.user import UserCreate
from tests.utils.utils import random_lower_string


def user_authentication_headers(server_api, email, password):
    data = {"username": email, "password": password}

    r = requests.post(f"{server_api}{config.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user():
    email = random_lower_string()
    password = random_lower_string()
    relation = random_lower_string()
    user_in = UserCreate(full_name=email, email=email, password=password, relation=relation)
    user = crud.user.create(db_session=db_session, user_in=user_in)
    return user
