from dash import Dash, html, dcc, Input, Output, State, exceptions, no_update
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
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


def create_blank_fig():
    blank_fig = go.Figure(
        go.Scatter(x=[],
                   y=[]),
        layout={"margin": dict(t=20, b=10, l=20, r=20),
                "height": 300,
                "xaxis_title": "",
                "yaxis_title": "",
                "font_size": 14})
    blank_fig.update_xaxes(range=[-3, 3])
    blank_fig.update_yaxes(range=[0, 1])
    return blank_fig


blank_fig = create_blank_fig()


app.layout = dbc.Container([
    dbc.Row([
        html.H1("Normal distribution")
    ], style={"padding": 20}),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="normal-dist-fig", style={"height": 300},
                      figure=blank_fig,
                      config={"displayModeBar": False})
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
            html.Br(),
            html.Br(),
            html.Label("Standard deviation: "),
            html.Br(),
            dcc.Input(id="sigma",
                      value=1,
                      type="number"),
            html.Br(),
            html.Br(),
            dbc.Button(id="submit",
                       n_clicks=0,
                       children="View distribution")
        ], xs=12, sm=6, md=6, lg=3, xl=3),
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
            html.Label("z1: "),
            html.Br(),
            dcc.Input(id="z-value1", type="number", value=None, disabled=True),
            html.Br(),
            html.Label("z2: "),
            html.Br(),
            dcc.Input(id="z-value2", type="number", value=None, disabled=True),
            html.Br(),
            html.Br(),
            dbc.Button(id="calculate",
                       n_clicks=0,
                       children="Calculate probability")
        ], xs=12, sm=6, md=6, lg=3, xl=3, id="z-input", style={"display": "none"})
    ])
])


@app.callback(
    Output("normal-dist-fig", "figure"),
    Output("z-input", "style"),
    Output("z-calc", "children"),
    Output("z-output", "style"),
    Input("submit", "n_clicks"),
    Input("calculate", "n_clicks"),
    State("mu", "value"),
    State("sigma", "value"),
    State("calc-type", "value"),
    State("z-value1", "value"),
    State("z-value2", "value"),
    prevent_initial_call=True
)
def generate_normal_dist(n_clicks_submit, n_clicks_calc, mu, sigma, calc_type, z1, z2):
    if n_clicks_submit is None or n_clicks_calc is None:
        raise exceptions.PreventUpdate
    x = np.linspace(stat.norm(mu, sigma).ppf(0.0001),
                    stat.norm(mu, sigma).ppf(0.9999),
                    10000)
    norm_x = stat.norm(mu, sigma).pdf(x)
    fig = go.Figure(
        go.Scatter(x=x, y=norm_x),
        layout={"margin": dict(t=20, b=10, l=20, r=20),
                "height": 300,
                "font_size": 14})
    if calc_type is None:
        return fig, {"display": "inline"}, no_update, no_update
    else:
        x1 = stat.norm(mu, sigma).cdf(z1)
        if calc_type == "<":
            probability = x1
            prob_less_than_x1 = np.linspace(
                stat.norm(mu, sigma).ppf(0.0001),
                stat.norm(mu, sigma).ppf(x1),
                10000)
            norm_pdf = stat.norm(mu, sigma).pdf(prob_less_than_x1)
            fig.add_trace(
                go.Scatter(x=prob_less_than_x1,
                           y=norm_pdf,
                           fill="tozeroy"))
        elif calc_type == ">":
            probability = 1 - x1
            prob_greater_than_x1 = np.linspace(
                stat.norm(mu, sigma).ppf(x1),
                stat.norm(mu, sigma).ppf(0.9999),
                10000)
            norm_pdf = stat.norm(mu, sigma).pdf(prob_greater_than_x1)
            fig.add_trace(
                go.Scatter(x=prob_greater_than_x1,
                           y=norm_pdf,
                           fill="tozeroy"))
        elif calc_type == "<>":
            max_z = max(z1, z2)
            min_z = min(z1, z2)
            x1 = stat.norm(mu, sigma).cdf(max_z)
            x2 = stat.norm(mu, sigma).cdf(min_z)
            probability = x1 - x2
            prob_between_x1_x2 = np.linspace(
                stat.norm(mu, sigma).ppf(x1),
                stat.norm(mu, sigma).ppf(x2),
                10000)
            norm_pdf = stat.norm(mu, sigma).pdf(prob_between_x1_x2)
            fig.add_trace(
                go.Scatter(x=prob_between_x1_x2,
                           y=norm_pdf,
                           fill="tozeroy"))
        else:
            x2 = stat.norm(mu, sigma).cdf(z2)
            probability = x1 + (1 - x2)
            prob_less_than_x1 = np.linspace(
                stat.norm(mu, sigma).ppf(0.0001),
                stat.norm(mu, sigma).ppf(x1),
                10000)
            norm_pdf1 = stat.norm(mu, sigma).pdf(prob_less_than_x1)
            prob_greater_than_x2 = np.linspace(
                stat.norm(mu, sigma).ppf(x2),
                stat.norm(mu, sigma).ppf(0.9999),
                10000)
            norm_pdf2 = stat.norm(mu, sigma).pdf(prob_greater_than_x2)
            fig.add_trace(
                go.Scatter(x=prob_less_than_x1,
                           y=norm_pdf1,
                           fill="tozeroy"))
            fig.add_trace(
                go.Scatter(x=prob_greater_than_x2,
                           y=norm_pdf2,
                           fill="tozeroy"))
        return fig, {"display": "inline"}, probability, {"display": "inline"}


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


if __name__ == "__main__":
    app.run(debug=True)
