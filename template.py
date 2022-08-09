from dash import Dash, html, dcc, Input, Output, State, exceptions, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import scipy.stats as stat

app = Dash(__name__,
           title="",
           update_title=None,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

app.layout = dbc.Container([
    dbc.Row([
        html.H1("Title")
    ]),
    dbc.Row([
        dbc.Col([

        ], xs=12, sm=12, md=12, lg=12, xl=12)
    ])
])


if __name__ == "__main__":
    app.run(debug=True)
