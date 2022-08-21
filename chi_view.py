from dash import Dash, html, dcc, Input, Output, State, exceptions, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import scipy.stats as stat
from chi_model import chi_happy

app = Dash(__name__,
           title="Association of categorical variables",
           update_title=None,
           external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

app.layout = dbc.Container([
    dbc.Row([
        html.H1("Association of categorical variables")
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Dependent variable (y axis)", className="label"),
            html.Div([
                dbc.Select(id="dependent",
                           options=[{"label": x, "value": x}
                                     for x in chi_happy.columns[1:7]],
                           value="UK_citizen"),
                dbc.FormFeedback(
                    "Dependent variable must be different to independent variable",
                    type="invalid")
            ], **{"aria-live": "polite"})
        ], xs=12, sm=6, md=4, lg=3, xl=3),
        dbc.Col([
            html.Label("Independent variable (x axis)", className="label"),
            html.Div([
                dbc.Select(id="independent",
                           options=[{"label": x, "value": x}
                                     for x in chi_happy.columns[1:7]],
                           value="Sex")
            ], **{"aria-live": "polite"}),
            html.Br()
        ], xs=12, sm=6, md=4, lg=3, xl=3),
        dbc.Col([
            html.H4("Results"),
            html.P(children=[
                html.Span("Chi squared: ", className="bold-p"),
                html.Span(id="chi2"),
                html.Span("P value: ", className="bold-p", style={"margin-left": 20}),
                html.Span(id="p-value")]),
            html.P([
                html.Span("Conclusion: ",
                        className="bold-p"),
                html.Span(id="acc-rej-h0")])
        ], xs=12, sm=12, md=4, lg=6, xl=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="graph",
                          config={"displayModeBar": False})
            ], role="img"),
            html.Br(),
            html.Div(id="sr-bar",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, sm=12, md=6, lg=6, xl=6),
        dbc.Col([
            html.Div([
                html.H4("Observed values"),
                html.Div(id="table-observed", children=[]),
                html.Br(),
                html.H4("Expected values"),
                html.Div(id="table-expected", children=[]),
                html.Br(),
                html.H4("Observed vs expected proportions"),
                html.Div(id="table-observed-pc", children=[])
            ], style={"padding-left": 30})
        ], xs=12, sm=12, md=6, lg=6, xl=6)
    ])
], fluid=True)
