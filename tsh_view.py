from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from tsh_model import happy_df

app = Dash(__name__,
           title="2-sample Hypothesis testing",
           update_title=None,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

app.layout = dbc.Container([
    dbc.Row([
        html.H1("2-sample Hypothesis testing")
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
                     **{"aria-live": "polite"}),
            html.Div([
                dcc.Graph(id="graph-hist2",
                          config={"displayModeBar": False})
            ], role="img"),
            html.Div(id="sr-hist2",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, sm=12, md=6, lg=6, xl=6),
        dbc.Col([
            html.Div([
                dcc.Dropdown(id="cols-dropdown",
                             options=[{"label": x, "value": x}
                                      for x in happy_df.columns[1:]],
                             value="Sex",
                             clearable=False)
            ], **{"aria-live": "polite"}),
            html.Label("Alternative hypothesis", className="label"),
            dcc.RadioItems(id="alternative",
                           options=[
                               {"label": u"Difference in means \u2260 0 (two-sided)",
                                "value": "!="},
                               {"label": "Difference in means < 0 (one-sided)",
                                "value": "<"},
                               {"label": "Difference in means > 0 (one-sided)",
                                "value": ">"}
                           ],
                           value="!=",
                           labelStyle={"display": "block",
                                       "margin-bottom": 5, "font-size": 16},
                           inputStyle={"margin-right": 10}),
            dbc.Button(id="submit",
                       n_clicks=0,
                       children="Update results",
                       class_name="button",
                       style={"width": 150}),
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
                html.P("Conclusion:", className="bold-p"),
                html.P(id="acc-rej-h0")
            ], id="results", style={"display": "none"}),
        ], xs=12, sm=12, md=12, lg=12, xl=6)
    ])
], fluid=True)


