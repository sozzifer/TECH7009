from dash import Dash, html, dcc, Input, Output, State, exceptions, dash_table, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import scipy.stats as stat

app = Dash(__name__,
           title="Normal distribution",
           update_title=None,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width,\
                                   initial-scale=1.0,\
                                   maximum-scale=1.0"
           }]
)

app.layout = dbc.Container([
    dbc.Row([
        html.H1("Normal distribution")
    ], style={"padding": 20}),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="normal-dist-fig", style={"height": 300})
        ], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([
            html.P(id="z-calc")
        ], id="z-output", xs=12, sm=12, md=12, lg=6, xl=6, style={"display": "none"})
    ]),
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Label("Mean: "),
            html.Br(),
            dcc.Input(id="mu",
                      value=0,
                      type="number"),
            dcc.Store(id="mu-store"),
            html.Br(),
            html.Br(),
            html.Label("Standard deviation: "),
            html.Br(),
            dcc.Input(id="sigma",
                      value=1,
                      type="number"),
            dcc.Store(id="sigma-store"),
            html.Br(),
            html.Br(),
            html.Button(id="submit",
                        n_clicks=0,
                        children="Submit")
        ]),
        dbc.Col([
            html.Br(),
            html.Label("Calculation type: "),
            html.Br(),
            dcc.RadioItems(id="calc-type",
                           options=[
                            {"label": "  Z < z1", "value": "<"},
                            {"label": "  Z > z1", "value": ">"},
                            {"label": "  z1 < Z < z2", "value": "<>"},
                            {"label": "  Z < z1 or Z > z2", "value": "><"}
                           ],
                           value=None,
                           labelStyle={"display": "block"}),
            html.Br(),
            html.Label("First Z value, z1: "),
            html.Br(),
            dcc.Input(id="z-value1", type="number", value=None, disabled=True),
            html.Br(),
            html.Label("Second Z value, z2: "),
            html.Br(),
            dcc.Input(id="z-value2", type="number", value=None, disabled=True),
            html.Br(),
            html.Br(),
            html.Button(id="calculate",
                        n_clicks=0,
                        children="Calculate")
        ], id="z-input", style={"display": "none"})
    ])
])


@app.callback(
    Output("normal-dist-fig", "figure"),
    Output("z-input", "style"),
    Output("mu-store", "data"),
    Output("sigma-store", "data"),
    Input("submit", "n_clicks"),
    State("mu", "value"),
    State("sigma", "value"),
)
def generate_normal_dist(n_clicks, mu, sigma):
    if not n_clicks:
        raise exceptions.PreventUpdate
    else:
        x = np.linspace(stat.norm(loc=mu, scale=sigma).ppf(0.0001),\
                        stat.norm(loc=mu, scale=sigma).ppf(0.9999),\
                        10000)
        norm_x = stat.norm(loc=mu, scale=sigma).pdf(x)
        fig = px.scatter(x=x, y=norm_x)
    return fig, {"display": "inline"}, mu, sigma


@app.callback(
    Output("z-value1", "disabled"),
    Output("z-value2", "disabled"),
    Input("calc-type", "value"),
    prevent_initial_call=True
)
def display_z_inputs(calc_type):
    if calc_type is None:
        raise exceptions.PreventUpdate
    if calc_type == "<>" or calc_type == "><":
        return False, False
    else:
        return False, True


@app.callback(
    Output("z-calc", "children"),
    Output("z-output", "style"),
    Input("calculate", "n_clicks"),
    State("calc-type", "value"),
    State("z-value1", "value"),
    State("z-value2", "value"),
    State("mu-store", "data"),
    State("sigma-store", "data"),
    prevent_initial_call=True
)
def z_calculation(n_clicks, calc_type, z1, z2, mu, sigma):
    if n_clicks is None:
        raise exceptions.PreventUpdate
    else:
        if calc_type == "<":
            x = stat.norm(loc=mu, scale=sigma).cdf(z1)
        elif calc_type == ">":
            x = 1 - stat.norm(loc=mu, scale=sigma).cdf(z1)
        elif calc_type == "<>":
            max_z = max(z1, z2)
            min_z = min(z1, z2)
            x = stat.norm(loc=mu, scale=sigma).cdf(max_z) - \
                stat.norm(loc=mu, scale=sigma).cdf(min_z)
        else:
            z_calc1 = stat.norm(loc=mu, scale=sigma).cdf(z1)
            z_calc2 = 1 - stat.norm(loc=mu, scale=sigma).cdf(z2)
            x = z_calc1 + z_calc2
        return x, {"display": "inline"}

if __name__ == "__main__":
    app.run(debug=True)
