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
    # dbc.Row([
    #     html.H1("Confidence Intervals")
    # ]),
    # dbc.Row([
    #     html.P(children=[
    #         "Completion of the Happiness questionnaire was voluntary, therefore the students who completed it can be considered a sample of a larger population - for example, the population of all students who have taken the Basic Data Analysis module. What conclusions can we draw about the population based on the Happy data set? One method is to find a ",
    #         html.Span("confidence interval (CI)", className="bold-p"),
    #         " of the mean for different variables."
    #     ])
    # ]),
    dbc.Row([
        html.H2("Confidence Intervals for quantitative variables"),
        html.P("Because of the large sample size, the confidence interval for the population mean of the variable of interest is quite narrow, even at the 99% confidence level. Select a variable from the dropdown list below to view upper and lower bounds for the actual value of its population mean.")
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(children=[
                dbc.Label("Variable",
                          className="label",
                          html_for="quant-dropdown"),
                dbc.Select(id="quant-dropdown",
                           options=[{"label": x, "value": x}
                                    for x in df_quant.columns[0:5]],
                           value="Total_happiness")
            ], id="quant-dropdown-div", **{"aria-live": "polite"}),
        ], xs=12, sm=12, md=4, lg=3, xl=3),
        dbc.Col([
            dbc.Label("Confidence level", className="label", html_for="quant-conf-value"),
            dcc.Slider(id="quant-conf-value",
                       value=0.95,
                       min=0.8,
                       max=0.99,
                       marks={0.8: {"label": "80%"},
                              0.85: {"label": "85%"}, 
                              0.9: {"label": "90%"}, 
                              0.95: {"label": "95%"},
                              0.99: {"label": "99%"}}),
        ], xs=12, sm=12, md=8, lg=9, xl=9)
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
        ], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([
            html.Div([
                dbc.Card([
                    dbc.CardBody(children=[
                        html.H4("Results"),
                        html.P(children=[
                            html.Span("Variable: ",
                                    className="bold-p"),
                            html.Span(id="quant-variable")
                        ]),
                        html.P(children=[
                            html.Span("Sample mean: ",
                                    className="bold-p"),
                            html.Span(id="quant-mean")
                        ]),
                        html.P(children=[
                            html.Span("Confidence interval for population mean: ",
                                    className="bold-p"),
                            html.Span(id="quant-conf-int")
                        ]),
                        html.P(children=[
                            html.Span("Confidence level: ",
                                    className="bold-p"),
                            html.Span(id="quant-conf-level")
                        ])
                    ])
                ])
            ], **{"aria-live": "polite"})
        ], xs=12, sm=12, md=12, lg=6, xl=6)
    ]),
    dbc.Row([
        html.H2("Confidence Intervals for qualitative variables"),
        html.P("When calculating confidence intervals for qualitative data, we are investigating if the probability of observing a specific characteristic is evenly distributed between categories, or if there are significant differences in the proportions in each category. For example, is a student completing the Happy questionnaire equally likely to be male or female? Select a variable from the dropdown list to view the observed proportions in each category, and compare this to categories with equal proportions.")
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Label("Variable",
                          className="label",
                          html_for="qual-dropdown"),
                dbc.Select(id="qual-dropdown",
                           options=[{"label": x, "value": x}
                                        for x in df_qual.columns[1:6]],
                           value="Sex")
            ], id="qual-dropdown-div", **{"aria-live": "polite"}),
            dbc.Label("Category",
                      className="label",
                      html_for="cat-radio"),
            dcc.RadioItems(id="cat-radio",
                           options=[],
                           labelStyle={"margin-left": 10},
                           inputStyle={"margin-right": 10})
        ], xs=12, sm=12, md=4, lg=3, xl=3),
        dbc.Col([
            dbc.Label("Confidence level",
                      className="label",
                      html_for="qual-conf-value"),
            dcc.Slider(id="qual-conf-value",
                       value=0.95,
                       min=0.8,
                       max=0.99,
                       marks={0.8: {"label": "80%"},
                              0.85: {"label": "85%"},
                              0.9: {"label": "90%"},
                              0.95: {"label": "95%"},
                              0.99: {"label": "99%"}}),
        ], xs=12, sm=12, md=8, lg=9, xl=9)
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
        ], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Results"),
                        html.P(children=[
                            html.Span("Variable: ",
                                      className="bold-p"),
                            html.Span(id="qual-variable")
                        ]), html.P(children=[
                            html.Span(id="qual-cat1", className="bold-p"),
                            html.Span(id="count-cat1")
                        ]),
                        html.P(children=[
                            html.Span(id="qual-cat2", className="bold-p"),
                            html.Span(id="count-cat2")
                        ]),
                        html.P(children=[
                            html.Span("Total count: ", className="bold-p"),
                            html.Span(id="qual-n-cat1")
                        ]),
                        html.P(children=[
                            html.Span(id="ci-cat1", className="bold-p"),
                            html.Span(id="qual-ci-result")
                        ]),
                        html.P(children=[
                            html.Span("Confidence level: ", className="bold-p"),
                            html.Span(id="qual-conf-level")
                        ])
                    ])
                ])
            ], **{"aria-live": "polite"})
        ], xs=12, sm=12, md=12, lg=6, xl=6)
    ])
], fluid=True)
