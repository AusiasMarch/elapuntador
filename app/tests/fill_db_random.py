import random
import datetime


import crud
from core import config

from models.altura import AlturaCreate
from models.peso import PesoCreate
from models.temperatura import TemperaturaCreate
from models.toma import TomaCreate

from db.session import db_session

n_datapoints = 100
start_date = datetime.datetime(year=2020, month=1, day=1)
finish_date = datetime.datetime(year=2024, month=1, day=1)


user = crud.user.get_by_email(db_session, email=config.FIRST_SUPERUSER_MAIL)


altura_0 = 50
altura_fin = 110
for i_point in range(n_datapoints):
    dt = start_date + i_point * (finish_date - start_date) / n_datapoints
    centimetros = altura_0 + i_point * (altura_fin - altura_0) / n_datapoints * (1 + (random.random() * 0.3 - 0.15))

    altura_in = AlturaCreate(
        user_id=user.id,
        query_text='',
        ip='666.666.666.666',
        centimetros=centimetros,
        datetime=dt
    )
    altura = crud.altura.create(db_session, altura_in=altura_in)