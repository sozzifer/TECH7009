from dash import Dash, html, dcc, Input, Output, State, exceptions, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import scipy.stats as stat
from eci_model import get_df_qual, get_df_quant, df_qual, df_quant

app = Dash(__name__,
           title="Confidence Intervals",
           update_title=None,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

app.layout = dbc.Container([
    dbc.Row([
        html.H1("Confidence Intervals")
    ]),
    dbc.Row([
        html.P("Completion of the Happiness questionnaire was voluntary, therefore the students who completed it can be considered a sample of a larger population - for example, the population of all students who have taken the Basic Data Analysis module. What conclusions can we draw about the population based on the Happy dataset? One method is to find a confidence interval (CI) of the mean for different variables.")
    ]),
    dbc.Row([
        html.H2("Confidence Intervals for quantitative variables")
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Variable"),
            html.Br(),
            html.Div(id="quant-dropdown-div",
                     children=[dcc.Dropdown(id="quant-dropdown",
                                            options=[{"label": x, "value": x}
                                                     for x in df_quant.columns[0:7]],
                                            value="tothappy",
                                            clearable=False)],
                     **{"aria-live": "polite"}),
            html.Br()
        ], xs=12, sm=12, md=2, lg=2, xl=2),
        dbc.Col([
            html.Label("Confidence level"),
            html.Br(),
            dcc.Slider(id="quant-conf-value",
                       value=0.95,
                       min=0.8,
                       max=0.99,
                       marks={0.8: {"label": "80%"},
                              0.85: {"label": "85%"}, 
                              0.9: {"label": "90%"}, 
                              0.95: {"label": "95%"},
                              0.99: {"label": "99%"}}),
            html.Br()
        ], xs=12, sm=12, md=10, lg=10, xl=10)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="quant-hist",
                          config={"displayModeBar": False})
            ], role="img"),
            html.Div(id="text-hist",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"}),
            html.Br(),
            html.Br()
        ], xs=12, sm=12, md=12, lg=8, xl=8),
        dbc.Col([
            html.Br(),
            html.P(id="quant-variable", children=[]),
            html.P(id="quant-mean", children=[]),
            html.P(id="quant-conf-int", children=[]),
            html.P(id="quant-conf-level", children=[])
        ], xs=12, sm=12, md=12, lg=4, xl=4)
    ]),
    dbc.Row([
        html.H2("Confidence Intervals for qualitative variables")
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Variable"),
            html.Br(),
            html.Div(id="qual-dropdown-div",
                     children=[dcc.Dropdown(id="qual-dropdown",
                                            options=[{"label": x, "value": x}
                                                     for x in df_qual.columns[1:6]],
                                            value="sex",
                                            clearable=False)],
                     **{"aria-live": "polite"}),
            html.Br()
        ], xs=12, sm=12, md=2, lg=2, xl=2),
        dbc.Col([
            html.Label("Confidence level"),
            html.Br(),
            dcc.Slider(id="qual-conf-value",
                       value=0.95,
                       min=0.8,
                       max=0.99,
                       marks={0.8: {"label": "80%"},
                              0.85: {"label": "85%"},
                              0.9: {"label": "90%"},
                              0.95: {"label": "95%"},
                              0.99: {"label": "99%"}}),
            html.Br()
        ], xs=12, sm=12, md=10, lg=10, xl=10)
    ]), 
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="qual-bar",
                          config={"displayModeBar": False})
            ], role="img"),
            html.Div(id="text-bar",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, sm=12, md=12, lg=8, xl=8),
        dbc.Col([
            html.Br(),
            html.P(id="qual-proportion1", children=[]),
            html.P(id="qual-proportion2", children=[]),
            html.P(id="qual-population", children=[]),
            html.P(id="qual-conf-int", children=[]),
            html.P(id="qual-conf-level", children=[])
        ], xs=12, sm=12, md=12, lg=4, xl=4)
    ])
])
