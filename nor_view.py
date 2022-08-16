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
        ], xs=12, sm=12, md=12, lg=4, xl=4),
        dbc.Col([
            html.Div([
            dcc.Graph(id="normal-dist-fig",
                      figure=create_blank_fig(),
                      config={"displayModeBar": False})
            ], role="img"),
            html.Div(id="sr-norm",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, sm=12, md=12, lg=8, xl=8)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Mean", className="label"),
            dbc.Input(id="mu",
                      value=0,
                      type="number",
                      required=True,
                      debounce=True),
            html.Label("Standard deviation", className="label"),
            dbc.Input(id="sigma",
                      value=1,
                      min=0.1,
                      type="number",
                      required=True,
                      debounce=True)
        ], xs=5, sm=5, md=4, lg=2, xl=2),
        dbc.Col([
            html.Label("Calculation type", className="label"),
            dcc.RadioItems(id="calc-type",
                           options=[
                               {"label": "  Z < z1",
                                "value": "<",
                                "title": "Z less than z1"},
                               {"label": "  Z > z1",
                                "value": ">",
                                "title": "Z greater than z1"},
                               {"label": "  z1 < Z < z2",
                                "value": "<>",
                                "title": "Z greater than z1 and less than z2"},
                               {"label": "  Z < z1 or Z > z2",
                                "value": "><",
                                "title": "Z less than z1 and greater than z2"}
                           ],
                           value=None,
                           labelStyle={"display": "block", "margin-bottom": 5})
        ], xs=4, sm=4, md=4, lg=2, xl=2),
        dbc.Col([
            html.Label("z1", className="label"),
            dbc.Input(id="z1",
                      type="number",
                      value=None,
                      disabled=True,
                      min=-4,
                      max=4,
                      required=False),
            html.Label("z2", className="label"),
            dbc.Input(id="z2",
                      type="number",
                      value=None,
                      disabled=True,
                      min=-4,
                      max=4,
                      required=False)
        ], xs=3, sm=3, md=2, lg=2, xl=2),
        dbc.Col([
            html.Br(),
            dbc.Button(id="submit",
                       n_clicks=0,
                       children="Submit",
                       class_name="button",
                       style={"width": 100}),
        ], xs=6, sm=6, md=2, lg=2, xl=2),
        dbc.Col([
            html.Br(),
            html.Div([
                html.P(id="current-mu", children=[]),
                html.P(id="current-sigma", children=[]),
                html.P(id="probability", children=[])
            ], id="output", style={"display": "none"}, **{"aria-live": "polite"})
        ], xs=6, sm=6, md=2, lg=2, xl=2),
        dbc.Col([], xs=0, sm=0, md=2, lg=2, xl=2)
    ])
], fluid=True)
