import logging
from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import HTMLResponse
from sqlalchemy.orm import Session

import crud
from api.utils.db import get_db
from api.utils.security import get_current_user
from core import config
from core.jwt import create_access_token
from core.security import get_password_hash
from db_models.users import Users as DBUser
from models.msg import Msg
from models.token import Token
from models.user import User
from utils import generate_password_reset_token, verify_password_reset_token
from myemails import send_reset_password_email

router = APIRouter()


log = logging.getLogger('elapuntador')



@router.get("/login", content_type=HTMLResponse)
def login(db: Session = Depends(get_db)):
    with open("/home/pi/elapuntador/app/html/login.html") as html:
        return html.read()


@router.post("/login/access-token", response_model=Token, tags=["login"])
def login_access_token(
        db: Session = Depends(get_db),
        # *,
        # body: dict,
        # form_data: dict,
        # form_data: OAuth2PasswordRequestForm = Depends()
):
    log.debug("yeah")
    log.debug(body)
    
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"user_id": users.id}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", tags=["login"], response_model=User)
def test_token(current_user: DBUser = Depends(get_current_user)):
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}", tags=["login"], response_model=Msg)
def recover_password(email: str, db: Session = Depends(get_db)):
    """
    Password Recovery
    """
    user = crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", tags=["login"], response_model=Msg)
def reset_password(
    token: str = Body(...), new_password: str = Body(...), db: Session = Depends(get_db)
):
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return {"msg": "Password updated successfully"}
