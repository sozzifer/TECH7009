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
            dbc.Card([
                dbc.CardBody(children=[
                    "This tool will allow you to view the area under the normal distribution curve  for different values of z1 and z2. To use standard units, set the mean as 0 and the standard deviation as 1.",
                    html.Br(),
                    html.Br(),
                    "Select a calculation type and enter values for z1 and z2 as indicated. The shaded area represents the probability that Z satisfies the given conditions.",
                    html.Br(),
                    html.Br(),
                    "Pay particular attention to how the scales of the x and y axes change when you enter different values for the mean, standard deviation, z1, and z2."
                ])
            ]),
            
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
            dbc.Card([
                dbc.CardBody([
                    html.H4("Results"),
                    html.Div([
                        html.P(children=[
                            html.Span("Mean: ", className="bold-p"),
                            html.Span(id="current-mu")
                        ]),
                        html.P(children=[
                            html.Span("Standard deviation: ",
                                      className="bold-p"),
                            html.Span(id="current-sigma")
                        ]),
                        html.P(children=[
                            html.Span("Probability: ", className="bold-p"),
                            html.Span(id="probability")
                        ]),
                    ], id="output", style={"display": "none"}, **{"aria-live": "polite"})
                ])
            ])
        ], xs=12, sm=12, md=12, lg=4, xl=4),
        dbc.Col([
            dbc.Label("Mean", className="label", html_for="mu"),
            dbc.Input(id="mu",
                      value=0,
                      type="number",
                      required=True,
                      debounce=True),
            dbc.Label("Standard deviation", className="label", html_for="sigma"),
            dbc.Input(id="sigma",
                      value=1,
                      min=0.1,
                      type="number",
                      required=True,
                      debounce=True)
        ], xs=4, sm=4, md=4, lg=2, xl=2),
        dbc.Col([
            dbc.Label("Calculation type", className="label", html_for="calc-type"),
            html.Div([
                dbc.RadioItems(id="calc-type",
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
                                     "title": "Z less than z1 and greater than z2"}],
                               value="<",
                               label_style={"display": "block", "margin-bottom": 5})
            ], **{"aria-live": "polite"})
        ], xs=5, sm=5, md=4, lg=2, xl=2),
        dbc.Col([
            html.Div([
                dbc.Label("z1", className="label", html_for="z1"),
                dbc.Input(id="z1",
                        type="number",
                        value=None,
                        disabled=False,
                        min=-4,
                        max=4,
                        required=True),
                dbc.Label("z2", className="label", html_for="z2"),
                dbc.Input(id="z2",
                        type="number",
                        value=None,
                        disabled=True,
                        min=-4,
                        max=4,
                        required=False),
                dbc.FormFeedback(id="error", children=[], type="invalid")
            ])
        ], xs=3, sm=3, md=2, lg=2, xl=2),
        dbc.Col([
            html.Br(),
            html.Div([dbc.Button(id="submit",
                       n_clicks=0,
                       children="Submit",
                       class_name="button",
                       style={"width": 100})
            ], className="d-flex justify-content-center")
        ], xs=12, sm=12, md=2, lg=2, xl=2)
    ], class_name="justify-content-right")
], fluid=True)
