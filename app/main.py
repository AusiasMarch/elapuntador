from fastapi import FastAPI

import models as models
import tasks as tasks

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/peso")
async def insert_note(peso: models.peso.PesoCreate):
    print(peso)
    return tasks.peso.insert_new(peso)