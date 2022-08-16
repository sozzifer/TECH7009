from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from eci_model import df_qual, df_quant

app = Dash(__name__,
           title="Confidence Intervals",
           update_title=None,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

app.layout = dbc.Container([
    dbc.Row([
        html.H1("Confidence Intervals")
    ]),
    dbc.Row([
        html.P(children=[
            "Completion of the Happiness questionnaire was voluntary, therefore the students who completed it can be considered a sample of a larger population - for example, the population of all students who have taken the Basic Data Analysis module. What conclusions can we draw about the population based on the Happy data set? One method is to find a ",
            html.Span("confidence interval (CI)", className="bold-p"),
            " of the mean for different variables."
        ])
    ]),
    dbc.Row([
        html.H2("Confidence Intervals for quantitative variables"),
        html.P("Because of the large sample size, the confidence interval for the population mean of is quite narrow, even at the 99% confidence level. Select a variable from the dropdown list below to view upper and lower bounds for its mean value.")
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Variable", className="label"),
            html.Div(id="quant-dropdown-div",
                     children=[dcc.Dropdown(id="quant-dropdown",
                                            options=[{"label": x, "value": x}
                                                     for x in df_quant.columns[0:7]],
                                            value="Total_happiness",
                                            clearable=False)],
                     **{"aria-live": "polite"}),
        ], xs=12, sm=12, md=4, lg=2, xl=2),
        dbc.Col([
            html.Label("Confidence level", className="label"),
            dcc.Slider(id="quant-conf-value",
                       value=0.95,
                       min=0.8,
                       max=0.99,
                       marks={0.8: {"label": "80%"},
                              0.85: {"label": "85%"}, 
                              0.9: {"label": "90%"}, 
                              0.95: {"label": "95%"},
                              0.99: {"label": "99%"}}),
        ], xs=12, sm=12, md=8, lg=10, xl=10)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="quant-hist",
                          config={"displayModeBar": False})
            ], role="img"),
            html.Br(),
            html.Div(id="sr-hist",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"}),
        ], xs=12, sm=12, md=12, lg=8, xl=8),
        dbc.Col([
            html.Div([
                html.P(id="quant-variable", children=[]),
                html.P(id="quant-mean", children=[]),
                html.P(id="quant-conf-int", children=[]),
                html.P(id="quant-conf-level", children=[])
            ], **{"aria-live": "polite", "aria-atomic": "true"})
        ], xs=12, sm=12, md=12, lg=4, xl=4)
    ]),
    dbc.Row([
        html.H2("Confidence Intervals for qualitative variables"),
        html.P("When calculating confidence intervals for qualitative data, we are trying to find out if the probability of observing a specific characteristic is evenly distributed between categories, or if there are significant differences in the proportions in each category. For example, is a student completing the Happy questionnaire equally likely to be male or female? Select a variable from the dropdown list to view the observed proportions in each category, and compare this to categories with equal proportions.")
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Variable", className="label"),
            html.Div(id="qual-dropdown-div",
                     children=[dcc.Dropdown(id="qual-dropdown",
                                            options=[{"label": x, "value": x}
                                                     for x in df_qual.columns[1:6]],
                                            value="Sex",
                                            clearable=False)],
                     **{"aria-live": "polite"}),
            html.Label("Category", className="label"),
            dcc.RadioItems(id="cat-radio",
                           options=[],
                           labelStyle={"margin-left": 10},
                           inputStyle={"margin-right": 10})
        ], xs=12, sm=12, md=4, lg=2, xl=2),
        dbc.Col([
            html.Label("Confidence level", className="label"),
            dcc.Slider(id="qual-conf-value",
                       value=0.95,
                       min=0.8,
                       max=0.99,
                       marks={0.8: {"label": "80%"},
                              0.85: {"label": "85%"},
                              0.9: {"label": "90%"},
                              0.95: {"label": "95%"},
                              0.99: {"label": "99%"}}),
        ], xs=12, sm=12, md=8, lg=10, xl=10)
    ]), 
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="qual-bar",
                          config={"displayModeBar": False})
            ], role="img"),
            html.Br(),
            html.Div(id="sr-bar",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, sm=12, md=12, lg=8, xl=8),
        dbc.Col([
            html.Div([
                html.P(id="qual-proportion1", children=[]),
                html.P(id="qual-proportion2", children=[]),
                html.P(id="qual-population", children=[]),
                html.P(id="qual-conf-int", children=[]),
                html.P(id="qual-conf-level", children=[])
            ], **{"aria-live": "polite", "aria-atomic": "true"})
        ], xs=12, sm=12, md=12, lg=4, xl=4)
    ])
], fluid=True)
