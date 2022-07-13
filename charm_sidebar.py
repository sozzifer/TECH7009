# Code source: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px
import pandas as pd


df = pd.read_csv("data/iranian_students.csv")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


sidebar = html.Div([
    html.H2("Sidebar", className="display-4"),
    html.Hr(),
    html.P("Number of students per education level", className="lead"),
    dbc.Nav([
        dbc.NavLink("Kindergarten", href="/", active="exact"),
        dbc.NavLink("Grade School", href="/grade", active="exact"),
        dbc.NavLink("High School", href="/high", active="exact"),
    ],
        vertical=True,
        pills=True,
    ),
],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
            html.H1("Kindergarten in Iran",
                    style={"textAlign": "center"}),
            dcc.Graph(id="bargraph",
                      figure=px.bar(df,
                                    barmode="group",
                                    x="Years",
                                    y=["Girls Kindergarten", "Boys Kindergarten"]))
        ]
    elif pathname == "/grade":
        return [
            html.H1("Grade School in Iran",
                    style={"textAlign": "center"}),
            dcc.Graph(id="bargraph",
                      figure=px.bar(df,
                                    barmode="group",
                                    x="Years",
                                    y=["Girls Grade School", "Boys Grade School"]))
        ]
    elif pathname == "/high":
        return [
            html.H1("High School in Iran",
                    style={"textAlign": "center"}),
            dcc.Graph(id="bargraph",
                      figure=px.bar(df,
                                    barmode="group",
                                    x="Years",
                                    y=["Girls High School", "Boys High School"]))
        ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Card(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True, port=3000)
