from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

app = Dash(__name__,
           title="Probability",
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

blank_fig = go.Figure(
    go.Scatter(x=[],
               y=[]),
    layout={"margin": dict(t=20, b=10, l=20, r=20), "height": 300})

app.layout = dbc.Container([
    dbc.Row(html.H1("Probability")),
    dbc.Row(html.P('The probability of winning a raffle with n tickets, where you buy x tickets, and one winning ticket is drawn, is x/n. Enter the total number of tickets (n) and the number of tickets bought (x) in the fields below, and click "Draw" 10 times. Is the observed win rate the same as the expected win rate? What about if you click "Draw" 20 times? 50 times?')),
    dbc.Row(children=[
        dbc.Col([
            html.Label("Enter number of tickets bought (x)",
                       style={"margin": 5}),
            dbc.Input(id="num-tickets",
                      value=3,
                      type="number",
                      min=1),
            dcc.Store(id="num-store"),
            html.Label("Enter total number of tickets (n)",
                       style={"margin": 5}),
            dbc.Input(id="total-tickets",
                      value=10,
                      type="number",
                      min=1),
            dcc.Store(id="total-store"),
            html.Label("Enter number draws",
                       style={"margin": 5}),
            dbc.Input(id="num-draws",
                      value=1,
                      type="number",
                      min=1),
            dcc.Store(id="draw-store"),
            html.Br()
        ], xs=12, sm=12, md=12, lg=4, xl=4),
        dbc.Col([
            dcc.Store(id="click-store"),
            dcc.Store(id="prob-store"),
            dcc.Store(id="win-store"),
            html.Button(id="submit",
                        n_clicks=0,
                        children="Draw"),
            html.Br(),
            html.Br(),
            html.P(id="probability"),
            html.P(id="win-rate"),
            html.P(id="draws")
        ], xs=12, sm=12, md=6, lg=4, xl=4),
        dbc.Col([
            html.P(id="my-tickets"),
            html.P(id="winning-ticket")
        ], xs=12, sm=12, md=6, lg=4, xl=4)
    ], class_name="justify-content-center"),
    dbc.Row([
        dcc.Graph(id="graph",
                  figure=blank_fig,
                  config={"displayModeBar": False}
                  )
    ], class_name="justify-content-center")
])
