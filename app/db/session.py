from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from core import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
