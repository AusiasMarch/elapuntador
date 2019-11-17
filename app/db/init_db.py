import datetime
import crud
from core import config
from core import external_data
from models.user import UserCreate
from models.sujeto import SujetoCreate
from db.base import Base
from db.session import engine

# make sure all SQL Alchemy models are imported before initializing DB
# otherwise, SQL Alchemy might fail to initialize properly relationships
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db_session):
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    Base.metadata.create_all(bind=engine)
    
    user = crud.user.get_by_email(db_session, email=config.FIRST_SUPERUSER_MAIL)
    if not user:
        user_in = UserCreate(
            email=config.FIRST_SUPERUSER_MAIL,
            password=config.FIRST_SUPERUSER_PASSWORD,
            full_name=config.FIRST_SUPERUSER_NAME,
            is_superuser=True,
            can_report=True,
            relation=config.FIRST_SUPERUSER_RELATION
        )
        user = crud.user.create(db_session, user_in=user_in)
    sujeto = crud.sujeto.get_by_name(db_session, name=config.FIRST_SUJETO_NAME)
    if not sujeto:
        sujeto_in = SujetoCreate(
            name=config.FIRST_SUJETO_NAME,
            apodos=config.FIRST_SUJETO_APODOS.split(','),
            birth=datetime.datetime.strptime(
                config.FIRST_SUJETO_BIRTH,
                '%Y-%m-%d %H:%M:%S'
            ),
        )
        sujeto = crud.sujeto.create(db_session, sujeto_in=sujeto_in)


import db
db_session = db.session.db_session
init_db(db_session)
external_data.download_who_data()
from app.tests.fill_db_random import fill
fill()