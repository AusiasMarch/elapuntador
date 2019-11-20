import os
import datetime
import plotly
import plotly.graph_objects as go


from db.session import db_session
import crud


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
    sujeto = crud.sujeto.get_by_apodo(db_session, apodo=apodo)
    data = data_sources[table](db_session=db_session, sujeto_id=sujeto.id)
    
    filename = "/tmp/elapuntador/{}_{}_{}.html".format(
        table,
        sujeto.name,
        data["datetime"].max()
    ).replace(" ", "_")
    
    if not os.path.exists(filename):
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
        
        fig = add_who(fig, sujeto, 'altura')
        
        fig.update_layout(
            xaxis_tickformat='%d %B %Y',
            title="{}'s {}}".format(sujeto.name, table),
            xaxis_title="Day",
            yaxis_title=table,
            # font=dict(
            #     family="Courier New, monospace",
            #     size=18,
            #     color="#7f7f7f"
            # )
        )
        
        plotly.offline.plot(fig, filename=filename, auto_open=False)
    
    with open(filename) as html:
        return html.read()