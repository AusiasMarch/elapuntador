import crud

from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from utils.db import get_db
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
    print(peso)