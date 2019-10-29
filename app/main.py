from fastapi import FastAPI

import models as models
import tasks as tasks
from core import config

app = FastAPI()

print(config.SQLALCHEMY_DATABASE_URI)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/peso")
async def insert_note(peso: models.peso.PesoCreate):
    print(peso)