from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from ssc_model import create_blank_fig

app = Dash(__name__,
           title="Student's t distribution",
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
        html.H1("Student's t distribution")
    ]),
    dbc.Row([
        dbc.Col([
            html.P("This tool will allow you to view the Student's t distribution curve for different confidence levels and degrees of freedom. To display the distribution, enter values for the mean and standard deviation and click Submit. Adjust the degrees of freedom and confidence level to see how this affects the confidence interval."),
            html.Br(),
            html.Div([
                html.P(id="current-mu", children=[]),
                html.P(id="current-sigma", children=[]),
                html.P(id="current-nu", children=[]),
                html.P(id="current-alpha", children=[]),
                html.P(id="probability", children=[])
            ], id="output", style={"display": "none"}, **{"aria-live": "polite"})
        ], xs=12, sm=12, md=3, lg=4, xl=4),
        dbc.Col([
            html.Div([
                dcc.Graph(id="t-dist-fig",
                          figure=create_blank_fig(),
                          config={"displayModeBar": False})
            ], role="img"),
            html.Div(id="sr-t",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, sm=12, md=9, lg=8, xl=8)
    ]),
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Label("Mean: ", htmlFor="mean"),
            html.Br(),
            dbc.Input(id="mu",
                      name="mean",
                      value=0,
                      type="number",
                      required=True,
                      debounce=True),
            html.Br(),
            html.Label("Standard deviation: ", htmlFor="standard-deviation"),
            html.Br(),
            dbc.Input(id="sigma",
                      name="standard-deviation",
                      value=1,
                      min=0.1,
                      type="number",
                      required=True,
                      debounce=True),
            html.Br(),
            dbc.Button(id="submit",
                       n_clicks=0,
                       children="Set mean and SD"),
        ], xs=4, sm=2, md=2, lg=4, xl=4),
        dbc.Col([
            html.Br(),
            html.Label("Degrees of freedom:"),
            dcc.Slider(id="nu",
                       value=10,
                       min=1,
                       max=40,
                       step=1,
                       marks={1: {"label": "1"},
                              5: {"label": "5"},
                              10: {"label": "10"},
                              20: {"label": "20"},
                              30: {"label": "30"},
                              40: {"label": "40"}},
                       disabled=True),
            html.Br(),
            html.Label("Confidence level:"),
            dcc.Slider(id="alpha",
                       value=0.95,
                       min=0.8,
                       max=0.99,
                       step=0.01,
                       marks={0.8: {"label": "80%"},
                              0.85: {"label": "85%"},
                              0.9: {"label": "90%"},
                              0.95: {"label": "95%"},
                              0.99: {"label": "99%"}},
                       disabled=True),
            html.Br()
        ], xs=12, sm=12, md=9, lg=8, xl=8)
    ])
])
