import random
import datetime


import crud
from core import config

from models.altura import AlturaCreate

from db.session import db_session

user = crud.user.get_by_email(db_session, email=config.FIRST_SUPERUSER_MAIL)
sujeto = crud.sujeto.get_by_name(db_session, name=config.FIRST_SUJETO_NAME)


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