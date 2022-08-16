from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dis_model import happy_df

app = Dash(__name__,
           title="Summarising and illustrating data",
           update_title=None,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

app.layout = dbc.Container([
    dbc.Row([
        html.H1("Summarising and illustrating data")
    ]),
    dbc.Row([
        html.P("The Happy data set contains 1170 responses to a questionnaire about students' levels of happiness on a scale of 0 to 28, as well as the student's sex, if they are a UK student or not, and whether they consider themselves to be extroverted/introverted, absorbed and bored. Select a categorical variable from the dropdown list below to compare total happiness for different groups.")
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Dropdown(id="cols-dropdown",
                             options=[{"label": x, "value": x}
                                      for x in happy_df.columns[1:]],
                             value="Sex",
                             clearable=False)
            ], **{"aria-live": "polite"})
        ], xs=6, sm=6, md=3, lg=3, xl=3)
    ], className="justify-content-center"),
    dbc.Row([
        dbc.Col([
            dbc.Button(id="toggle",
                       n_clicks=0,
                       children=[],
                       class_name="button")
        ], xs=6, sm=6, md=3, lg=3, xl=3)
    ], className="justify-content-center"),
    dbc.Row([
        dbc.Col([
            dbc.Collapse([
                html.Div([
                    dbc.Card([
                        dbc.CardBody([
                            html.Table(id="desc1",
                                       className="descriptive",
                                       children=["Hide Descriptive statistics"])
                        ])
                    ], id="card1", style={"margin": "auto"})
                ], **{"aria-live": "polite", "aria-atomic": "true"})
            ], className="justify-content-center", id="collapse1", is_open=True)
        ], xs=12, sm=12, md=6, lg=6, xl=6, style={"margin": "auto"}),
        dbc.Col([
            dbc.Collapse([
                html.Div([
                    dbc.Card([
                        dbc.CardBody([
                            html.Table(id="desc2",
                                       className="descriptive",
                                       children=[])
                        ])
                    ], id="card2", style={"margin": "auto"})
                ], **{"aria-live": "polite", "aria-atomic": "true"})
            ], className="justify-content-center", id="collapse2", is_open=True)
        ], xs=12, sm=12, md=6, lg=6, xl=6, style={"margin": "auto"})
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="graph-hist1",
                          config={"displayModeBar": False})
            ], role="img"),
            html.Div(id="sr-hist1",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, sm=12, md=6, lg=6, xl=6),
        dbc.Col([
            html.Div([
                dcc.Graph(id="graph-hist2",
                          config={"displayModeBar": False})
            ], role="img"),
            html.Div(id="sr-hist2",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, sm=12, md=6, lg=6, xl=6)
    ], id="hist-row"),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="graph-box1",
                          config={"displayModeBar": False})
            ], role="img"),
            html.Div(id="sr-box1",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, sm=12, md=6, lg=6, xl=6),
        dbc.Col([
            html.Div([
                dcc.Graph(id="graph-box2",
                          config={"displayModeBar": False})
            ], role="img"),
            html.Div(id="sr-box2",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, sm=12, md=6, lg=6, xl=6)
    ], id="box-row")
], fluid=True)
