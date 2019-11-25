import os
import yaml
import datetime
import crud
from core import external_data
from models.user import UserCreate
from models.sujeto import SujetoCreate
from models.location import LocationCreate
from models.coordinates import Coordinates
from db.base import Base
from db.session import engine

# make sure all SQL Alchemy models are imported before initializing DB
# otherwise, SQL Alchemy might fail to initialize properly relationships
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


fill_file = "_" if os.path.exists("_initial_fill.yaml") else ""
with open(f"{fill_file}initial_fill.yaml") as fill_input:
    fill_data = yaml.load(fill_input, Loader=yaml.FullLoader)


def init_db(db_session):
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    Base.metadata.create_all(bind=engine)

    for user_fill in fill_data['users']:
        user = crud.user.get_by_email(db_session, email=user_fill['email'])
        if not user:
            user_in = UserCreate(
                email=user_fill['email'],
                password=user_fill['password'],
                full_name=user_fill['name'],
                is_superuser=user_fill['is_superuser'],
                can_report=user_fill['can_report'],
                relation=user_fill['relation']
            )
            user = crud.user.create(db_session, user_in=user_in)

    for sujeto_fill in fill_data['sujetos']:
        sujeto = crud.sujeto.get_by_name(db_session, name=sujeto_fill['name'])
        if not sujeto:
            sujeto_in = SujetoCreate(
                name=sujeto_fill['name'],
                gender=sujeto_fill['gender'],
                apodos=sujeto_fill['apodos'],
                birth=datetime.datetime.strptime(
                    sujeto_fill['birth'],
                    '%Y-%m-%d %H:%M:%S'
                ),
            )
            sujeto = crud.sujeto.create(db_session, sujeto_in=sujeto_in)

    for location_fill in fill_data['locations']:
        location = crud.location.get_by_name(db_session, location_name=location_fill['name'])
        if not location:
            location_in = LocationCreate(
                name=location_fill['name'],
                center=Coordinates(
                    lat=location_fill['lat'],
                    lng=location_fill['lng']
                ),
                radius=location_fill['radius']
            )
            location = crud.location.create(db_session, location_in=location_in)


from db.session import db_session
init_db(db_session)

sujeto=crud.sujeto.get_by_name(db_session=db_session, name="Entropía")
coordinates = Coordinates(lat=41.582603, lng=1.628425)
crud.sujeto.update_latlng(db_session=db_session, sujeto=sujeto, coordinates=coordinates, car=False)
sujeto=crud.sujeto.get_by_apodo(db_session=db_session, apodo="Ausias")
coordinates = Coordinates(lat=41.582603, lng=1.628425)
crud.sujeto.update_latlng(db_session=db_session, sujeto=sujeto, coordinates=coordinates, car=False)
db_session.commit()
sujetos = crud.sujeto.get_all(db_session)

external_data.download_who_data()
from app.tests.fill_db_random import fill
fill()
