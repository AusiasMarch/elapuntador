from fastapi import FastAPI

import app.models as models
import app.tasks as tasks

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/peso")
async def insert_note(peso: models.peso.PesoCreate):
    return tasks.peso.insert_new(peso)