from typing import List, Optional

import crud

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from core.security import get_password_hash, verify_password
from db_models.user import User
from models.user import UserCreate, UserUpdate
from models.relation import RelationCreate


def get(db_session: Session, *, user_id: int) -> Optional[User]:
    return db_session.query(User).filter(User.id == user_id).first()


def get_by_email(db_session: Session, *, email: str) -> Optional[User]:
    print(email)
    return db_session.query(User).filter(User.email == email).first()


def authenticate(db_session: Session, *, email: str, password: str) -> Optional[User]:
    user = get_by_email(db_session, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def is_active(user) -> bool:
    return user.is_active


def is_superuser(user) -> bool:
    return user.is_superuser


def can_report(user) -> bool:
    return user.can_report


def get_multi(db_session: Session, *, skip=0, limit=100) -> List[Optional[User]]:
    return db_session.query(User).offset(skip).limit(limit).all()


def create(db_session: Session, *, user_in: UserCreate) -> User:
    relation = crud.relation.get_by_relation(
        db_session,
        relation=user_in.relation)
    if not relation:
        relation_in = RelationCreate(
            relation=user_in.relation
        )
        relation = crud.relation.create(db_session, relation_in=relation_in)
    
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_superuser=user_in.is_superuser,
        can_report=user_in.can_report,
        relation_id=relation.id
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def update(db_session: Session, *, user: User, user_in: UserUpdate) -> User:
    user_data = jsonable_encoder(user)
    update_data = user_in.dict(skip_defaults=True)
    for field in user_data:
        if field in update_data:
            setattr(user, field, update_data[field])
    if user_in.password:
        passwordhash = get_password_hash(user_in.password)
        user.hashed_password = passwordhash
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
