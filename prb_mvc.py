import numpy as np
import random
from dash import Dash, html, dcc, Input, Output, State, exceptions
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
    layout={"margin": dict(t=20, b=10)})


app.layout = dbc.Container([
    dbc.Row(id="row1", children=[
        html.H1("Probability"),
        dbc.Col([
            html.Label("Enter total number of tickets", style={"margin": 10}),
            dbc.Input(id="total-tickets",
                      value=10,
                      type="number",
                      min=1),
            html.Br(),
            html.Label("Enter number of tickets bought", style={"margin": 10}),
            dbc.Input(id="num-tickets",
                      value=3,
                      type="number",
                      min=1),
            html.Br(),
            html.Br()
        ], xs=12, sm=12, md=6, lg=6, xl=6),
        dbc.Col([
            html.Button(id="submit",
                        n_clicks=0,
                        children="Submit"),
            html.Br(),
            html.Br(),
            html.P(id="my-tickets"),
            html.P(id="winning-ticket"),
            html.P(id="probability"),
            html.P(id="win-rate"),
            dcc.Store(id="click-array"),
            dcc.Store(id="win-array"),
            dcc.Store(id="prob-array"),
            dcc.Store(id="total-store"),
            dcc.Store(id="num-store")
        ], xs=12, sm=12, md=6, lg=6, xl=6)
    ]),
    dbc.Row([
        dcc.Graph(id="graph",
                  figure=blank_fig,
                  config={"displayModeBar": False}
        )
    ])
])


@app.callback(
    Output("probability", "children"),
    Output("my-tickets", "children"),
    Output("winning-ticket", "children"),
    Output("win-rate", "children"),
    Output("click-array", "data"),
    Output("win-array", "data"),
    Output("prob-array", "data"),
    Output("graph", "figure"),
    Output("total-store", "data"),
    Output("num-store", "data"),
    Input("submit", "n_clicks"),
    State("total-tickets", "value"),
    State("num-tickets", "value"),
    State("win-array", "data"),
    State("click-array", "data"),
    State("prob-array", "data")
)
def generate_winner(n_clicks, total, num, win_array, click_array, prob_array):
    if not n_clicks:
        raise exceptions.PreventUpdate
    elif num > total:
        return "Tickets bought must be fewer than total tickets", "", "", "", click_array, win_array, prob_array, blank_fig
    else:
        probability = round((num/total)*100, 2)
        my_tickets = random.sample(range(1, int(total) + 1), int(num))
        winning_ticket = np.random.randint(1, int(total) + 1, size=(1))
        tickets_string = [str(x) for x in my_tickets]
        my_tickets_string = ", ".join(tickets_string)
        winner = False
        win_array = win_array or [0]
        click_array = click_array or [0]
        prob_array = prob_array or [0]
        for ticket in my_tickets:
            if ticket == winning_ticket:
                winner = True

        if winner == True:
            win_array.append(win_array[-1] + 1)
        else:
            win_array.append(win_array[-1])


        win_rate = round((win_array[-1]/n_clicks)*100, 2)
        click_array.append(n_clicks)
        prob_array.append((num/total)*n_clicks)
        print(f"n_clicks: {n_clicks}")
        print(f"total: {total}")
        print(f"num: {num}")
        print(f"win_array: {win_array}")
        print(f"click_array: {click_array}")
        print(f"prob_array: {prob_array}")
        fig = go.Figure()
        fig.update_layout(margin=dict(t=20, b=10))
        fig.add_trace(go.Scatter(x=click_array,
                                 y=win_array,
                                 name="Observed probability"))
        fig.add_trace(go.Scatter(x=click_array,
                                 y=prob_array,
                                 name="Calculated probability"))
        if winner == True:
            return f"Probability of winning: {probability}%", f"My tickets: {my_tickets_string}", f"Winning ticket: {winning_ticket[0]} - YOU WIN", f"Win rate: {win_rate}%", click_array, win_array, prob_array, fig, total, num
        return f"Probability of winning: {probability}%", f"My tickets: {my_tickets_string}", f"Winning ticket: {winning_ticket[0]}", f"Win rate: {win_rate}%", click_array, win_array, prob_array, fig, total, num


if __name__ == "__main__":
    app.run(debug=True)
