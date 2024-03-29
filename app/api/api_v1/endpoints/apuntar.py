import os
import logging
import datetime

from fastapi import APIRouter, Depends, Body, Header
from sqlalchemy.orm import Session
import crud
from api.utils.db import get_db
from models.peso import PesoCreate
from models.altura import AlturaCreate
from models.toma import TomaCreate
from models.temperatura import TemperaturaCreate
from models.apunte_response import Answer, BasicCard, ApunteResponse

from core import jwt
from core import config
from core import plots

log = logging.getLogger('elapuntador')


router = APIRouter()


@router.post("/", response_model=ApunteResponse, status_code=202)
def insert_apunte(
    *,
    body: dict,
    x_forwarded_for: str = Header(None),
    db_session: Session = Depends(get_db),
):
    log.debug(body)
    log.info("Recieving apunte.")
    id_token = body['originalDetectIntentRequest']['payload']['user']['idToken']
    decoded_token = jwt.decode_google_token(id_token)
    clientid = decoded_token['aud']
    iss = decoded_token['iss']
    if clientid != config.GOOGLE_CLIENTID:
        log.debug(f"Invalid Google Client ID {clientid}.")
        return {"msg": "Invalid Google Client ID."}
    if iss != config.GOOGLE_ISS:
        log.debug(f"Invalid Google ISS {iss}.")
        return {"msg": "Invalid Google ISS."}
    log.debug(decoded_token)
    user = crud.user.get_by_email(db_session=db_session, email=decoded_token['email'])
    log.debug("user: {}".format(user))
    # log.debug(body)
    log.debug(body['queryResult']['parameters'])
    if not user.can_report:
        return {"msg": f"The user {user.full_name} is not allowed to report."}
    sujeto = crud.sujeto.get_by_apodo(
        db_session=db_session,
        apodo=body['queryResult']['parameters']['sujeto']
    )
    
    if "donde" in body['queryResult']['parameters'].keys():
        log.debug("Is a donde query.")
        location = crud.location.get_by_sujeto(db_session=db_session, sujeto=sujeto)
        log.debug(location)
        return Answer(kind='location', sujeto=sujeto, location=location).content
    elif ("Que" in body['queryResult']['parameters'].keys() and
        "temperatura" in body['queryResult']['parameters'].keys()):
        filename, plot_datetime = plots.get_last_static(
            "temperatura",
            body['queryResult']['parameters']['sujeto']
        )
        plot_datetime = datetime.datetime.strftime(
            plot_datetime.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None),
            '%H:%M')
        
        temp = crud.temperatura.get_last_by_sujeto(db_session=db_session, sujeto=sujeto)
        
        card = BasicCard(
            content=f"La temperatura actual de {sujeto.name} es de {temp.grados} grados.",
            title=f"Temperatura de {sujeto.name} ({plot_datetime})",
            button_title="Full plot",
            button_url=os.path.join(
                "http://elapuntador.ddns.net",
                config.API_V1_STR,
                "dash",
                sujeto.name,
                "temperatura"
            ),
            image_text="Evolución de la temperatura",
            image_url=f"http://elapuntador.ddns.net/card_plots/{filename}"
        )
        log.debug(card.content)
        
        return card.content
    
    
    elif 'pesa' in body['queryResult']['parameters'].keys():
        kilos = body['queryResult']['parameters']['n_kilos']
        gramos = body['queryResult']['parameters']['n_gramos']
        peso_in = PesoCreate(
            user_id=user.id,
            sujeto_id=sujeto.id,
            query_text=body['queryResult']['queryText'],
            ip=x_forwarded_for,
            kilos=kilos if kilos else 0,
            gramos=gramos if gramos else 0,
        )
        crud.peso.create(db_session=db_session, peso_in=peso_in)
        
        return Answer(kind='peso', suejto=sujeto, kilos=kilos, gramos=gramos).content
    
    elif 'mide' in body['queryResult']['parameters'].keys():
        centimetros = body['queryResult']['parameters']['n_centimetros']
        altura_in = AlturaCreate(
            user_id=user.id,
            sujeto_id=sujeto.id,
            query_text=body['queryResult']['queryText'],
            ip=x_forwarded_for,
            centimetros=centimetros,
        )
        crud.altura.create(db_session=db_session, altura_in=altura_in)
        return Answer(kind='altura', suejto=sujeto, centimetros=centimetros).content
    
    elif 'tomado' in body['queryResult']['parameters'].keys():
        mililitros = body['queryResult']['parameters']['n_mililitros']
        toma_in = TomaCreate(
            user_id=user.id,
            sujeto_id=sujeto.id,
            query_text=body['queryResult']['queryText'],
            ip=x_forwarded_for,
            mililitros=mililitros,
        )
        crud.toma.create(db_session=db_session, toma_in=toma_in)
        return Answer(kind='toma', suejto=sujeto, mililitros=mililitros).content
    
    elif 'temperatura' in body['queryResult']['parameters'].keys():
        grados = body['queryResult']['parameters']['n_grados']
        decimas = body['queryResult']['parameters']['n_decimas']
        temperatura_in = TemperaturaCreate(
            user_id=user.id,
            sujeto_id=sujeto.id,
            query_text=body['queryResult']['queryText'],
            ip=x_forwarded_for,
            grados=grados,
            decimas=decimas
        )
        crud.temperatura.create(db_session=db_session, temperatura_in=temperatura_in)
        _, last_temp = plots.get_last_static("temperatura", sujeto.name)
        
        if last_temp is None or \
                datetime.datetime.now() - last_temp > datetime.timedelta(hours=1):
            plots.plot_static("temperatura", sujeto.name)
        
        return Answer(kind='temperatura', suejto=sujeto, grados=grados, decimas=decimas).content


    # from db.session import db_session
    # sujeto = crud.sujeto.get_by_apodo(
    #     db_session=db_session,
    #     apodo='sala'
    # )


# @router.get("/info", response_model=List[FitInfoDB], status_code=200)
# def get_fit_info(
#     offset: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db),
#     current_user: DBUser = Depends(get_current_active_superuser),
# ):
#     """
#     Paginated information about the fit history.
#     """
#     return crud.fit.read_multi(db_session=db, limit=limit, offset=offset)
#
#
# @router.get("/main", response_model=FitInfoDB, status_code=200)
# def get_main_fit(
#     db: Session = Depends(get_db),
#     current_user: DBUser = Depends(get_current_active_superuser),
# ):
#     """
#     Returns the actual main model fit, which is used as the default model for prediction
#     """
#     return crud.fit.read_main(db_session=db)
#
#
# @router.put("/main", response_model=FitInfoDB, status_code=200)
# def update_main_fit(
#     info_in: MainFit,
#     db: Session = Depends(get_db),
#     current_user: DBUser = Depends(get_current_active_superuser),
# ):
#     """
#     Updates the main model fit given an existing model ID
#     """
#     if not crud.fit.read(db_session=db, fit_id=info_in.fit_id):
#         raise HTTPException(status_code=404)
#     return _update_main_fit(db=db, fit_id=info_in.fit_id)
#
#
# @router.get("/{fit_id}/info", response_model=List[FitInfoDB], status_code=200)
# def get_fit_info(
#     fit_id: int,
#     db: Session = Depends(get_db),
#     current_user: DBUser = Depends(get_current_active_superuser),
# ):
#     """
#     Returns paginated information about the fit history.
#     If ID is informed the result is filtered by ID.
#     """
#     return crud.fit.read(db_session=db, fit_id=fit_id)
#
#
# @router.get("/{fit_id}/download", status_code=200)
# def get_fit(
#     fit_id: int,
#     db: Session = Depends(get_db),
#     current_user: DBUser = Depends(get_current_active_superuser),
# ):
#     fit = crud.fit.read(db, fit_id=fit_id)
#     if fit is None:
#         raise HTTPException(status_code=404)
#     models = crud.model.read_multi_by_fit(db_session=db, fit_id=fit_id)
#     filename = "fit_{}.zip".format(fit.id)
#     zip_file = generate_zip(
#         ["model_{}.pkl".format(model.id) for model in models],
#         [model.model for model in models],
#     )
#     return Response(
#         zip_file,
#         media_type="application/octet-stream",
#         headers={"Content-Disposition": 'attachment; filename="{}"'.format(filename)},
#     )
#
#
# def _update_main_fit(db: Session, fit_id: int):
#     """
#     Updates the main fit in DB
#     :param db: Database session
#     :param fit_id: New main fit fit ID
#     :return: new main fit as a DB object
#     """
#     main_fits = crud.fit.read_main(db_session=db)
#     updated = datetime.now()
#     for fit in main_fits:
#         crud.fit.update(
#             db, fit_id=fit.id, fit_in=FitInfoDBUpdate(
#                 updated=updated,
#                 is_main=False,
#             )
#         )
#     new_main = crud.fit.update(
#         db, fit_id=fit_id, fit_in=FitInfoDBUpdate(
#             updated=updated,
#             is_main=True,
#         )
#     )
#     return new_main
