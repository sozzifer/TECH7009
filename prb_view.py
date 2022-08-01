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
    dbc.Row(html.P('The probability of winning a raffle with n tickets, where you buy x tickets, and one winning ticket is drawn, is x/n. Enter the total number of tickets (n) and the number of tickets bought (x) in the fields below, and set the number of draws as 10. Is the observed win rate the same as the expected win rate? What about if you draw 20 times? 50 times?')),
    dbc.Row([
        dcc.Interval(id="interval",
                     interval=1*500,
                     max_intervals=0),
        dcc.Store(id="draw-store"),
        dcc.Store(id="win-store"),
        dcc.Store(id="prob-store"),
        dcc.Store(id="win-rate-store"),
        dcc.Store(id="my-tickets-store"),
        dcc.Store(id="winning-ticket-store"),
        dbc.Col([
            html.Label("Enter number of tickets bought, x (max 1000)",
                       className="label"),
            dbc.Input(id="num-tickets",
                      value=3,
                      type="number",
                      min=1,
                      max=1000),

            html.Label("Enter total number of tickets, n (max 1000)",
                       className="label"),
            dbc.Input(id="total-tickets",
                      value=10,
                      type="number",
                      min=1,
                      max=1000),

            html.Label("Enter number of draws (max 1000)",
                       className="label"),
            dbc.Input(id="num-draws",
                      value=5,
                      type="number",
                      min=1,
                      max=1000),

            html.Br()
        ], xs=12, sm=12, md=12, lg=4, xl=4),
        dbc.Col([
            html.Button(id="draw",
                        n_clicks=0,
                        children="Draw"),
            html.Br(),
            html.Br(),

            html.P(id="probability", children=[]),
            html.P(id="win-rate", children=[]),
            html.P(id="draws", children=[])

        ], xs=12, sm=12, md=6, lg=4, xl=4),
        dbc.Col([
            html.P(id="my-tickets"),
            html.P(id="winning-ticket")
        ], xs=12, sm=12, md=6, lg=4, xl=4)
    ]),
    dbc.Row([
        dcc.Graph(id="graph",
                  figure=blank_fig,
                  config={"displayModeBar": False}
                  )
    ])
])
