from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from car_model import df_quant

app = Dash(__name__,
           title="Correlation and Regression",
           update_title=None,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

app.layout = dbc.Container([
    dbc.Row([
        html.H1("Correlation and Regression")
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Dropdown(id="dropdown1",
                             options=[{"label": x, "value": x}
                                      for x in df_quant.columns[0:7]],
                             value="Height",
                             clearable=False)
            ], **{"aria-live": "polite"})
        ], xs=12, sm=12, md=12, lg=3, xl=3),
        dbc.Col([
            html.Div([
                dcc.Dropdown(id="dropdown2",
                             options=[{"label": x, "value": x}
                                      for x in df_quant.columns[0:7]],
                             value="Weight",
                             clearable=False)
            ], **{"aria-live": "polite"})
        ], xs=12, sm=12, md=12, lg=3, xl=3),
        dbc.Col([
            html.P(children=[
                html.Span("Regression equation: ", className="bold-p"),
                html.Span(id="results")
            ]),
            html.P(children=[
                html.Span("R-squared value: ", className="bold-p"),
                html.Span(id="r-squared")])
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="xy-graph",
                      config={"displayModeBar": False})
        ], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([
            dcc.Graph(id="res-graph",
                      config={"displayModeBar": False})
        ], xs=12, sm=12, md=12, lg=6, xl=6)
    ])
], fluid=True)

