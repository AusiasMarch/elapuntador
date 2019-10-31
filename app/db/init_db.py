import crud
from core import config
from models.user import UserCreate
from models.relation import RelationCreate
from db.base import Base
from db.session import engine

# make sure all SQL Alchemy models are imported before initializing DB
# otherwise, SQL Alchemy might fail to initialize properly relationships
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from db import base


def init_db(db_session):
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_email(db_session, email=config.FIRST_SUPERUSER)
    if not user:
        relation_id = crud.relation.get_by_relation(db_session, name=config.FIRST_SUPERUSER_RELATION).id
        if not relation_id:
            relation_id = RelationCreate(
                relation=config.FIRST_SUPERUSER_RELATION
            ).id
        user_in = UserCreate(
            email=config.FIRST_SUPERUSER,
            password=config.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            can_report=True,
            relation_id=relation_id
        )
        user = crud.user.create(db_session, user_in=user_in)


import db
init_db(db.session.db_session)