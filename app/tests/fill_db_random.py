import os
import yaml
import random
import datetime


import crud
from core import config

from models.altura import AlturaCreate

from db.session import db_session


fill_file = "_" if os.path.exists("_initial_fill.yaml") else ""
with open(f"{fill_file}initial_fill.yaml") as fill_input:
    fill_data = yaml.load(fill_input, Loader=yaml.FullLoader)

user = crud.user.get_by_name(db_session, name="Ausias March")
sujeto = crud.sujeto.get_by_apodo(db_session, apodo="Entropía")

n_datapoints = 100
start_date = sujeto.birth
finish_date = start_date + datetime.timedelta(days=365*4)

altura_0 = 50
altura_fin = 110

def fill():
    for i_point in range(n_datapoints):
        dt = start_date + i_point * (finish_date - start_date) / n_datapoints
        centimetros = altura_0 + i_point * (altura_fin - altura_0) / n_datapoints * (1 + (random.random() * 0.3 - 0.15))
    
        altura_in = AlturaCreate(
            sujeto_id=sujeto.id,
            user_id=user.id,
            query_text='',
            ip='666.666.666.666',
            centimetros=centimetros,
            datetime=dt
        )
        altura = crud.altura.create(db_session, altura_in=altura_in)