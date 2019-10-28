import crud
from db.session import get_db_session

from models.peso import PesoCreate



def insert_new(peso_in: PesoCreate):
    db = get_db_session()
    
    return crud.peso.insert_peso(db, peso_in=peso_in)