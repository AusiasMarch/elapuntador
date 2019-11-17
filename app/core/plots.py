import os
import datetime
import plotly
import plotly.graph_objects as go

from fastapi import Depends
from sqlalchemy.orm import Session

import crud
from api.utils.db import get_db


# from db.session import db_session

def altura(
    db_session: Session = Depends(get_db),
    apodo: str = 'Entropía',):
    sujeto = crud.sujeto.get_by_apodo(db_session, apodo=apodo)
    
    alturas = crud.altura.get_all(db_session)
    alturas_who = crud.altura_who.get_all_girls(db_session)
    alturas_who['datetime'] = alturas_who.index.map(
        lambda x: datetime.timedelta(days=x)) + sujeto.birth
    
    filename = "/tmp/elapuntador/altura_{}_{}.html".format(
        sujeto.name,
        alturas["datetime"].max()
    ).replace(" ", "_")
    
    if not os.path.exists(filename):
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=alturas.datetime.dt.to_pydatetime(),
                y=alturas.centimetros.values,
                line=dict(width=5, color='black'),
                mode='lines+markers',
                name='Measured'
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=alturas_who.datetime.dt.to_pydatetime(),
                y=alturas_who['P50'].values,
                line=dict(width=3, color='green', dash='dot'),
                mode='lines+markers',
                name='Media',
            )
        )
        
        for percentile in 'P25', 'P75':
            fig.add_trace(
                go.Scatter(
                    x=alturas_who.datetime.dt.to_pydatetime(),
                    y=alturas_who[percentile].values,
                    line=dict(width=3, color='orange', dash='dot'),
                    mode='lines+markers',
                    name=percentile,
                )
            )
        
        for percentile in 'P10', 'P90':
            fig.add_trace(
                go.Scatter(
                    x=alturas_who.datetime.dt.to_pydatetime(),
                    y=alturas_who[percentile].values,
                    line=dict(width=3, color='red', dash='dot'),
                    mode='lines+markers',
                    name=percentile,
                )
            )
        fig.update_layout(xaxis_tickformat='%d %B %Y')
        
        plotly.offline.plot(fig, filename=filename, auto_open=False)
    
    with open(filename) as html:
        return html.read()