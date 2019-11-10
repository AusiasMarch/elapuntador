from fastapi import APIRouter, Depends, Body, Header
from sqlalchemy.orm import Session
from crud import altura
from api.utils.db import get_db

from core import jwt
from starlette.authentication import AuthenticationError
from core import config


import plotly
import plotly.graph_objects as go
import pandas as pd


router = APIRouter()


@router.get("/dash")
def insert_apunte(
    *,
    db_session: Session = Depends(get_db),
):
    crud_alt = altura.get_all(db_session)
    print(crud_alt)
    print(crud_alt[0])
    
    alturas = pd.DataFrame(
        [(x.datetime, x.centimetros, x.ip, x.user_id, x.user.full_name) for x in
         crud_alt],
        columns=['datetime', 'centimetros', 'ip', 'user_id', 'user_name'],
        index=[(x.id) for x in crud_alt]
    )
    
    fig = go.Figure([go.Scatter(x=alturas['datetime'], y=alturas['centimetros'])])
    # plotly.offline.plot(
    #     fig,
    #     filename="/tmp/altura.html",
    #     auto_open=True,
    # )
    
    
    
    return fig


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
