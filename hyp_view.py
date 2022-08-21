from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from hyp_model import age

app = Dash(__name__,
           title="1-sample Hypothesis Testing",
           update_title=None,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

blank_fig = go.Figure(go.Histogram(x=age,
                                   xbins={"start": 5, "end": 65, "size": 10},
                                   name="Age (years)",
                                   marker_line_color="rgba(158,171,5,1)",
                                   marker_color="rgba(158,171,5,0.5)",
                                   marker_line_width=1),
                      layout={"margin": dict(t=20, b=10, l=20, r=20),
                              "height": 400,
                              "font_size": 14})

app.layout = dbc.Container([
    dbc.Row([
        html.H1("1-sample Hypothesis Testing")
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="graph",
                        figure=blank_fig,
                        config={"displayModeBar": False})
            ], role="img"),
            html.Div(id="sr-hist",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, sm=12, md=12, lg=12, xl=8),
        dbc.Col([
            html.H4("Results", style={"text-align": "center"}),
            html.Br(),
            html.Div([
                html.P(children=[
                    html.Span("Test statistic: ", className="bold-p"),
                    html.Span(id="t-stat")
                ]),
                html.P(children=[
                    html.Span("P value: ", className="bold-p"),
                    html.Span(id="p-value")
                ]),
                html.P(children=[
                    html.Span(id="conf-text", className="bold-p"),
                    html.Span(id="conf-val")
                ]),
                html.P("Conclusion:", className="bold-p"),
                html.P(id="acc-rej-h0"),
            ], id="results", style={"display": "none"})
        ], xs=12, sm=12, md=12, lg=12, xl=4)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Data set", className="label"),
            dcc.Dropdown(id="dropdown",
                         options=[{"label": "Age", "value": "age"},
                                 {"label": "RDA", "value": "rda"},
                                 {"label": "Antacid", "value": "antacid"}],
                         value="age",
                         clearable=False),
            html.Label("Hypothesised mean", className="label"),
            dbc.Input(id="hyp-mean",
                      value=None,
                      type="number",
                      required=True),
            html.Label("Confidence level", className="label"),
            dcc.Slider(id="alpha",
                       value=0.95,
                       min=0.8,
                       max=0.99,
                       marks={0.8: {"label": "80%"},
                              0.85: {"label": "85%"},
                              0.9: {"label": "90%"},
                              0.95: {"label": "95%"},
                              0.99: {"label": "99%"}})
        ], xs=12, sm=12, md=12, lg=12, xl=6),
        dbc.Col([
            html.Label("Alternative hypothesis", className="label"),
            dcc.RadioItems(id="alternative",
                           options=[
                               {"label": u"Population mean \u2260 hypothesised mean (two-sided)",
                                "value": "!="},
                               {"label": "Population mean < hypothesised mean (one-sided)",
                                "value": "<"},
                               {"label": "Population mean > hypothesised mean (one-sided)",
                                "value": ">"}
                           ],
                           value="!=",
                           labelStyle={"display": "block", "margin-bottom": 5, "font-size": 16},
                           inputStyle={"margin-right": 10}),
            dbc.Button(id="submit",
                       n_clicks=0,
                       children="Update results",
                       class_name="button",
                       style={"width": 150})
        ], xs=12, sm=12, md=12, lg=12, xl=6)
    ])
], fluid=True)
