from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from prb_model import create_blank_fig

app = Dash(__name__,
           title="Probability",
           update_title=None,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

blank_fig = create_blank_fig()

app.layout = dbc.Container([
    dbc.Row(html.H1("Probability")),
    dbc.Row([
        dcc.Interval(id="interval",
                     interval=1000,
                     max_intervals=0),
        dcc.Store(id="draw-store"),
        dcc.Store(id="win-store"),
        dcc.Store(id="prob-store"),
        dcc.Store(id="win-rate-store"),
        dcc.Store(id="my-tickets-store"),
        dcc.Store(id="winning-ticket-store"),
        dbc.Col([
            html.P("The probability of winning a raffle with n tickets, where you buy x tickets, and one winning ticket is drawn, is x/n."),
            html.P("Enter the total number of tickets (n) and the number of tickets bought (x), and set the number of draws as 10. Is the observed win rate the same as the expected win rate? What about if you draw 20 times? 50 times?")
        ], xs=12, sm=12, md=12, lg=3, xl=3),
        dbc.Col([
            html.Div([
                dcc.Graph(id="graph",
                          figure=blank_fig,
                          config={"displayModeBar": False})
            ], role="img"),
            html.Div(id="sr-graph",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, sm=12, md=12, lg=9, xl=9)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Enter number of tickets bought, x (max 1000)",
                       className="label"),
            dbc.Input(id="num-tickets",
                      value=3,
                      type="number",
                      min=1,
                      max=1000,
                      step=1,
                      required=True),
            html.P(id="error",
                   children="Tickets bought must be fewer than total tickets",
                   className="error"),
            html.Label("Enter total number of tickets, n (max 1000)",
                       className="label"),
            dbc.Input(id="total-tickets",
                      value=10,
                      type="number",
                      min=1,
                      max=1000,
                      step=1,
                      required=True),
            html.Label("Enter number of draws (max 100)",
                       className="label"),
            dbc.Input(id="num-draws",
                      value=10,
                      type="number",
                      min=1,
                      max=100,
                      step=1,
                      required=True)
        ], xs=12, sm=12, md=12, lg=4, xl=4),
        dbc.Col([
            html.Label("Set number of draws per second",
                       className="label"),
            dcc.Slider(id="slider",
                       min=10,
                       max=100,
                       step=10,
                       value=10),
            html.Div([
                dbc.Button(id="draw",
                           n_clicks=0,
                           children="Draw",
                           class_name="button"),
                dbc.Button(id="stop",
                           n_clicks=0,
                           children="Stop",
                           class_name="button")
            ], style={"margin": "0 auto"}),
            html.Br(),
            html.Div([
                html.Div(id="probability",
                         style={"display": "inline",
                                "margin-right": 20}),
                html.Div(id="win-rate",
                         style={"display": "inline",
                                "margin-right": 20}),
                html.Div(id="draws",
                         style={"display": "inline",
                                "margin-right": 20})
            ], style={"display": "inline-block"}, **{"aria-live": "polite"})
        ], xs=12, sm=12, md=12, lg=8, xl=8)
    ])
], fluid=True)
