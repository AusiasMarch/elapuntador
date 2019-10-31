from app import crud
from app.db.session import db_session
from app.models.peso import PesoCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_peso(user_id: int = None):
    if user_id is None:
        user = create_random_user()
        user_id = user.id
    title = random_lower_string()
    description = random_lower_string()
    item_in = PesoCreate(title=title, description=description, id=id)
    return crud.peso.create(db_session=db_session, peso_in=item_in, user_id=user_id)
