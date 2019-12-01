import os
import datetime
import plotly
import plotly.graph_objects as go
import logging


from db.session import db_session
import crud


log = logging.getLogger('elapuntador')

who = {
    'altura': {
        'girl': crud.altura_who.get_all_girls,
        'boy': crud.altura_who.get_all_boys
    },
    'peso': {
        'girl': crud.peso_who.get_all_girls,
        'boy': crud.peso_who.get_all_boys
    },
}

data_sources = {
    'altura': crud.altura.get_all_by_sujeto,
    'peso': crud.peso.get_all_by_sujeto
}

units ={
    "altura": "cm",
    "peso": "kg",
    "temperatura": "º"
}


def add_who(fig, sujeto, table):
    expected = who[table][sujeto.gender](db_session)
    expected['datetime'] = expected.index.map(
        lambda x: datetime.timedelta(days=x)) + sujeto.birth

    fig.add_trace(
        go.Scatter(
            x=expected.datetime.dt.to_pydatetime(),
            y=expected['P50'].values,
            line=dict(width=3, color='green', dash='dot'),
            mode='lines+markers',
            name='Media',
        )
    )
    
    for percentile in 'P25', 'P75':
        fig.add_trace(
            go.Scatter(
                x=expected.datetime.dt.to_pydatetime(),
                y=expected[percentile].values,
                line=dict(width=3, color='orange', dash='dot'),
                mode='lines+markers',
                name=percentile,
            )
        )
    
    for percentile in 'P10', 'P90':
        fig.add_trace(
            go.Scatter(
                x=expected.datetime.dt.to_pydatetime(),
                y=expected[percentile].values,
                line=dict(width=3, color='red', dash='dot'),
                mode='lines+markers',
                name=percentile,
            )
        )
    
    return fig


def plot(
        table: str,
        apodo: str,
):
    log.debug(f"Plotting {table} for {apodo}.")
    sujeto = crud.sujeto.get_by_apodo(db_session, apodo=apodo)
    data = data_sources[table](db_session=db_session, sujeto_id=sujeto.id)
    
    filename = f"/tmp/elapuntador/{table}_{sujeto.name}_{data['datetime'].max()}.html"\
        .replace(" ", "_")
    
    if not os.path.exists(filename):
        log.debug(
            f"The plot {table} for {apodo} does not exists or is not updated. "
            "Creating it."
        )
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=data.datetime.dt.to_pydatetime(),
                y=data.centimetros.values,
                line=dict(width=5, color='black'),
                mode='lines+markers',
                name='Measured'
            )
        )
        
        if table in who.keys():
            fig = add_who(fig, sujeto, 'altura')
        
        fig.update_layout(
            xaxis_tickformat='%d %B %Y',
            title=f"{sujeto.name}'s {table}s",
            xaxis_title="Day",
            yaxis_title=f"{table.title()} [{units[table]}]",
            # font=dict(
            #     family="Courier New, monospace",
            #     size=18,
            #     color="#7f7f7f"
            # )
        )
        
        plotly.offline.plot(fig, filename=filename, auto_open=False)
        fig.write_image(filename[:-4] + 'png')
    else:
        log.debug(f"The plot {table} for {apodo} already exists. ")
    
    with open(filename) as html:
        return html.read()