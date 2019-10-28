import app.crud as crud
from app.db.session import get_db_session

from app.models.peso import PesoCreate



def insert_new(peso_in: PesoCreate):
    db = get_db_session()
    
    return crud.peso.insert_peso(db, peso_in=peso_in)