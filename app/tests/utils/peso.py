import random

from app import crud
from app.db.session import db_session
from app.models.peso import PesoCreate
from app.tests.utils.user import create_random_user


def create_random_peso(user_id: int = None):
    if user_id is None:
        user = create_random_user()
        user_id = user.id
    kilos = random.randint(0, 10)
    gramos = random.randint(0, 99) * 10
    peso_in = PesoCreate(user_id=user_id, kilos=kilos, gramos=gramos)
    return crud.peso.create(db_session=db_session, peso_in=peso_in)
