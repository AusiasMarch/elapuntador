from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from core.security import get_password_hash, verify_password
from db_models.reporter import Reporter
from models.reporter import ReporterCreate, ReporterUpdate


def get(db_session: Session, *, reporter_id: int) -> Optional[Reporter]:
    return db_session.query(Reporter).filter(Reporter.id == reporter_id).first()


def get_by_email(db_session: Session, *, email: str) -> Optional[Reporter]:
    return db_session.query(Reporter).filter(Reporter.email == email).first()


def authenticate(db_session: Session, *, email: str, password: str) -> Optional[Reporter]:
    reporter = get_by_email(db_session, email=email)
    if not reporter:
        return None
    if not verify_password(password, reporter.hashed_password):
        return None
    return reporter


def is_active(reporter) -> bool:
    return reporter.is_active


def is_superuser(reporter) -> bool:
    return reporter.is_superuser


def get_multi(db_session: Session, *, skip=0, limit=100) -> List[Optional[Reporter]]:
    return db_session.query(Reporter).offset(skip).limit(limit).all()


def create(db_session: Session, *, reporter_in: ReporterCreate) -> Reporter:
    reporter = Reporter(
        email=reporter_in.email,
        hashed_password=get_password_hash(reporter_in.password),
        full_name=reporter_in.full_name,
        is_superuser=reporter_in.is_superuser,
    )
    db_session.add(reporter)
    db_session.commit()
    db_session.refresh(reporter)
    return reporter


def update(db_session: Session, *, reporter: Reporter, reporter_in: ReporterUpdate) -> Reporter:
    reporter_data = jsonable_encoder(reporter)
    update_data = reporter_in.dict(skip_defaults=True)
    for field in reporter_data:
        if field in update_data:
            setattr(reporter, field, update_data[field])
    if reporter_in.password:
        passwordhash = get_password_hash(reporter_in.password)
        reporter.hashed_password = passwordhash
    db_session.add(reporter)
    db_session.commit()
    db_session.refresh(reporter)
    return reporter
