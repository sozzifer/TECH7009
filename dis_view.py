from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dis_model import happy_df

app = Dash(__name__,
           title="Total happiness",
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

app.layout = dbc.Container([
    dbc.Row([
        html.H1("Summarising and illustrating data")
    ], style={"padding": 20}),
    dbc.Row([
        html.P("The Happy dataset contains 1170 responses to a questionnaire about students' levels of happiness on a scale of 0 to 28, as well as the student's sex, if they are a UK student or not, and whether they consider themselves to be extroverted/introverted, absorbed and bored. Select a categorical variable from the dropdown list below to compare total happiness for different groups.")
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id="cols-dropdown",
                         options=[{"label": x, "value": x}
                                  for x in happy_df.columns[1:]],
                         value="Sex",
                         clearable=False)
        ], style={"margin":"auto"}, xs=12, sm=3, md=3, lg=3, xl=3)
    ], class_name="justify-content-center"),
    dbc.Row([
        dbc.Col([
            html.H3("Descriptive statistics"),
            html.H3(id="header1"),
            html.Table(className="desc", children=[
                html.Tr([html.Td(className="mean", children=["Mean:"]),
                        html.Td(id="mean1")]),
                html.Tr([html.Td(className="median", children=["Median:"]),
                        html.Td(id="median1")]),
                html.Tr([html.Td(className="std", children=["Standard deviation:"]),
                        html.Td(id="std1")]),
                html.Tr([html.Td(className="q1", children=["First quartile:"]),
                        html.Td(id="q1_1")]),
                html.Tr([html.Td(className="q3", children=["Third quartile:"]),
                        html.Td(id="q3_1")]),
                html.Tr([html.Td(className="iqr", children=["Interquartile range:"]),
                        html.Td(id="iqr1")]),
            ])
        ], xs=6, sm=6, md=6, lg=6, xl=6),
        dbc.Col([
            html.H3("Descriptive statistics"),
            html.H3(id="header2"),
            html.Table(className="desc", children=[
                html.Tr([html.Td(className="mean", children=["Mean:"]),
                        html.Td(id="mean2")]),
                html.Tr([html.Td(className="median", children=["Median:"]),
                        html.Td(id="median2")]),
                html.Tr([html.Td(className="std", children=["Standard deviation:"]),
                        html.Td(id="std2")]),
                html.Tr([html.Td(className="q1", children=["First quartile:"]),
                        html.Td(id="q1_2")]),
                html.Tr([html.Td(className="q3", children=["Third quartile:"]),
                        html.Td(id="q3_2")]),
                html.Tr([html.Td(className="iqr", children=["Interquartile range:"]),
                        html.Td(id="iqr2")]),
            ])
        ], xs=6, sm=6, md=6, lg=6, xl=6)
    ], style={"padding": 20}),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="output-hist1")
        ], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([
            dcc.Graph(id="output-hist2")
        ], xs=12, sm=12, md=12, lg=6, xl=6)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="output-box1")
        ], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([
            dcc.Graph(id="output-box2")
        ], xs=12, sm=12, md=12, lg=6, xl=6)
    ])
])
