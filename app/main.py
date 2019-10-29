import crud

from fastapi import FastAPI
from db.session import db_session

import models as models
from core import config


app = FastAPI()

print(config.SQLALCHEMY_DATABASE_URI)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/peso")
def insert_note(
        *,
        peso_in: models.peso.PesoCreate):
    
    peso = crud.peso.create(db_session=db_session, peso_in=peso_in)
    
@app.get("/get_pesos")
async def root():
    
    pesos = crud.peso.get_all(db_session=db_session)
    for peso in pesos:
        print(peso.reporter())
    
    return pesos