from dash import Dash, html, dcc, Input, Output, exceptions
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np


app = Dash(__name__,
           title="Normal distribution",
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
            dcc.Graph(id="placeholder", style={"height": 300})
        ], xs=12, sm=12, md=12, lg=6, xl=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Label("Mean: "),
            html.Br(),
            dcc.Input(id="mean",
                      value=0,
                      type="number"),
            html.Br(),
            html.Br(),
            html.Label("Standard deviation: "),
            html.Br(),
            dcc.Input(id="std",
                      value=1,
                      type="number"),
            html.Br(),
            html.Br(),
            html.Label("Sample size: "),
            html.Br(),
            dcc.Input(id="size",
                      value=1000,
                      type="number"),
            html.Br(),
            html.Br()

        ]),
        dbc.Col([
            html.Br(),
            html.Br(),
            html.Button(id="submit",
                        n_clicks=0,
                        children="Submit")
        ]),
        dbc.Col([]),
        dbc.Col([]),
    ])
])


@app.callback(
    Output("normal-dist-fig", "figure"),
    Input("mean", "value"),
    Input("std", "value"),
    Input("size", "value"),
    Input("submit", "n_clicks")
)
def generate_normal_hist(mean, std, size, n_clicks):
    if not n_clicks:
        raise exceptions.PreventUpdate
    else:
        data = np.random.default_rng().normal(mean, std, size)
        fig = px.histogram(data)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
