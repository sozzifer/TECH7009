from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from nor_model import create_blank_fig

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
    ]),
    dbc.Row([
        dbc.Col([
            html.P("This tool will allow you to view the area under the normal distribution curve  for different values of z1 and z2. To use standard units, set the mean as 0 and the standard deviation as 1. Select a calculation type and enter values for z1 and z2 as indicated. The shaded area represents the probability that Z satisfies the given conditions.")
        ], xs=12, sm=12, md=3, lg=4, xl=4),
        dbc.Col([
            dcc.Graph(id="normal-dist-fig",
                      figure=create_blank_fig(),
                      config={"displayModeBar": False})
        ], xs=12, sm=12, md=9, lg=8, xl=8)
    ]),
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Label("Mean: "),
            html.Br(),
            dbc.Input(id="mu",
                      value=0,
                      type="number",
                      required=True,
                      debounce=True),
            html.Br(),
            html.Label("Standard deviation: "),
            html.Br(),
            dbc.Input(id="sigma",
                      value=1,
                      min=0.1,
                      type="number",
                      required=True,
                      debounce=True)
        ], xs=4, sm=2, md=2, lg=2, xl=2),
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
                           labelStyle={"display": "block"})
        ], xs=4, sm=3, md=2, lg=2, xl=2),
        dbc.Col([
            html.Br(),
            html.Label("z1: "),
            html.Br(),
            dbc.Input(id="z1", type="number", value=None,
                      disabled=True, min=-4, max=4, required=False),
            html.Br(),
            html.Label("z2: "),
            html.Br(),
            dbc.Input(id="z2", type="number", value=None,
                      disabled=True, min=-4, max=4, required=False)
        ], xs=4, sm=2, md=2, lg=2, xl=2),
        dbc.Col([
            html.Br(),
            dbc.Button(id="submit",
                       n_clicks=0,
                       children="Submit"),
            html.Br(),
            html.Br(),
            html.Div([
                html.P(id="current-mu", children=[]),
                html.P(id="current-sigma", children=[]),
                html.P(id="probability", children=[])
            ], id="output", style={"display": "none"})
        ], xs=12, sm=3, md=2, lg=2, xl=2)
    ])
])
