import crud
from core import config
from models.reporter import ReporterCreate
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

    reporter = crud.reporter.get_by_email(db_session, email=config.FIRST_SUPERUSER)
    if not reporter:
        reporter_in = ReporterCreate(
            email=config.FIRST_SUPERUSER,
            password=config.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        reporter = crud.reporter.create(db_session, reporter_in=reporter_in)


import db
init_db(db.session.get_db_session())