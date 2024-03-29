import os
import datetime
import plotly
import plotly.graph_objects as go
import logging
import seaborn as sns
import matplotlib.pyplot as plt

from db.session import db_session
import crud


log = logging.getLogger('elapuntador')


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)



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
    'peso': crud.peso.get_all_by_sujeto,
    'temperatura': crud.temperatura.get_all_by_sujeto,
}

units = {
    "altura": "cm",
    "peso": "kg",
    "temperatura": "º"
}

variable = {
    "altura": "centimetros",
    "peso": "kilos",
    "temperatura": "grados"
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


def get_data(apodo: str, table: str, previous_days: int=1000):
    sujeto = crud.sujeto.get_by_apodo(db_session, apodo=apodo)
    data = data_sources[table](db_session=db_session, sujeto_id=sujeto.id, previous_days=previous_days)
    data = data.sort_values("datetime")
    data["datetime"] = data["datetime"].apply(utc_to_local)
    if table == 'temperatura':
        data['grados'] = data['grados'] + data['decimas'] / 10
    elif table == 'peso':
        data['kilos'] = data['kilos'] + data['gramos'] / 100

    return data, sujeto


def plot_dynamic(
        table: str,
        apodo: str
):
    log.debug(f"Plotting {table} for {apodo}.")
    
    data, sujeto = get_data(apodo, table)
    delta_t = data.datetime.max() - data.datetime.min()
    xaxis_tickformat = "%b-%d %H:%M" if delta_t < datetime.timedelta(days=3) \
        else "%Y-%b-%d"
    
    filename = f"/tmp/elapuntador/{table}_{sujeto.name}_{data['datetime'].max()}.html"\
        .replace(" ", "_")
    
    if not os.path.exists(filename):
        log.debug(
            f"The plot {table} for {apodo} does not exist or is not updated. "
            "Creating it."
        )
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=data.datetime.dt.to_pydatetime(),
                y=data[variable[table]].values,
                line=dict(width=5, color='black'),
                mode='lines+markers',
                name='Measured'
            )
        )
        
        if table in who.keys():
            fig = add_who(fig, sujeto, table)
        
        if table == "temperatura":
            fig.add_trace(
                go.Scatter(
                    x=[data.datetime.dt.to_pydatetime().min(),
                       data.datetime.dt.to_pydatetime().max()],
                    y=[data[variable[table]].mean(),
                       data[variable[table]].mean()],
                    line=dict(width=5, color='red'),
                    mode='lines',
                    name='Average'
                )
            )

        fig.update_layout(
            xaxis_tickformat=xaxis_tickformat,
            title=f"{sujeto.name}'s {table}s",
            xaxis_title="Time",
            yaxis_title=f"{table.title()} [{units[table]}]",
        )
        
        plotly.offline.plot(fig, filename=filename, auto_open=False)
    else:
        log.debug(f"The plot {table} for {apodo} already exists.")
    
    with open(filename) as html:
        return html.read()
    

def plot_static(table: str, apodo: str):
    log.debug(f"Plotting {table} for {apodo}.")

    data, sujeto = get_data(apodo, table, previous_days=3)
    
    filename = os.path.join(
        "/tmp/elapuntador/",
        f"{table}_{sujeto.name}_{data['datetime'].max()}.png".replace(" ", "_")
    )

    log.debug(f"Searching for {filename}.")

    if not os.path.exists(filename):
        log.debug(f"The plot {filename} does not exist. Making it.")
        sns.set_context("poster")
        plt.clf()
        ax = sns.lineplot(
            x=data.datetime.dt.to_pydatetime(),
            y=data[variable[table]],
            sort=True, lw=5
        )
        ax.axhline(data[variable[table]].mean(), ls='--', color='red')
        fig = ax.get_figure()
        fig.autofmt_xdate()
        sns.set_context("notebook", font_scale=1.5)
        fig.savefig(filename, dpi=192, bbox_inches="tight")
    else:
        log.debug(f"The plot {filename} already exists. ")

    return filename.split("/")[-1]


def filter_plot(plot: str, table: str, sujeto_name: str, extension: str = None):
    p_table, p_sujeto_name, p_date, p_time = plot.split("_")
    if p_table == table and p_sujeto_name == sujeto_name:
        if extension is None:
            return True
        else:
            if p_time.endswith(extension):
                return True
            else:
                return False
    else:
        return False


def get_last_static(table: str, apodo: str):
    sujeto_name = crud.sujeto.get_by_apodo(db_session, apodo=apodo).name
    plots = os.listdir("/tmp/elapuntador")
    plots = [x for x in plots if filter_plot(x, table, sujeto_name, '.png')]
    if len(plots) == 0:
        return None, None
    plot = sorted(plots)[-1]
    plot_date, plot_time = plot.split("_")[2:4]
    plot_time = plot_time.split(".")[0]
    
    plot_datetime = datetime.datetime.strptime(
        f"{plot_date} {plot_time}",
        "%Y-%m-%d %H:%M:%S"
    )
    return plot, plot_datetime


# import matplotlib.pyplot as plt
# plt.clf()
# table='temperatura'
# apodo='sala'
# plot_static(table, apodo)