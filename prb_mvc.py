import numpy as np
import random
from dash import Dash, html, dcc, Input, Output, State, exceptions
import dash_bootstrap_components as dbc

app = Dash(__name__,
           title="Probability",
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

app.layout = dbc.Container([
    dbc.Row(id="row1", children=[
        html.H1("Probability"),
        dbc.Col([
            html.Label("Enter total number of tickets", style={"margin": 10}),
            dcc.Input(id="total-tickets",
                      value=10,
                      type="number"),
            html.Br(),
            html.Br()
        ], xs=12, sm=12, md=12, lg=4, xl=4),
        dbc.Col([
            html.Label("Enter number of tickets bought", style={"margin": 10}),
            dcc.Input(id="num-tickets",
                      value=3,
                      type="number"),
            html.Br(),
            html.Br()
        ], xs=12, sm=12, md=12, lg=4, xl=4),
        dbc.Col([
            html.Button(id="submit",
                        n_clicks=0,
                        children="Submit"),
            html.Br(),
            html.Br(),
            html.P(id="probability"),
            html.P(id="my-tickets"),
            html.P(id="winning-ticket"),
            html.P(id="winner")
        ], xs=12, sm=12, md=12, lg=4, xl=4)
    ])
])

@app.callback(
    Output(component_id="probability", component_property="children"),
    Output(component_id="my-tickets", component_property="children"),
    Output(component_id="winning-ticket", component_property="children"),
    Output(component_id="winner", component_property="children"),
    Input(component_id="submit", component_property="n_clicks"),
    State(component_id="total-tickets", component_property="value"),
    State(component_id="num-tickets", component_property="value"),
)
def generate_winner(n_clicks, total, num):
    if not n_clicks:
        raise exceptions.PreventUpdate
    else:
        if num > total:
            return "Tickets bought must be fewer that total tickets", "", "", ""
        else:
            probability = round((num/total)*100, 2)
            my_tickets = random.sample(range(1, int(total) + 1), int(num))
            string_tickets = [str(x) for x in my_tickets]
            my_tickets_string = ", ".join(string_tickets)
            winning_ticket = np.random.randint(1, int(total) + 1, size=(1))
            winner = False
            for ticket in my_tickets:
                if ticket == winning_ticket:
                    winner = True
            if winner == True:
                return f"Probability of winning: {probability}%", f"My tickets: {my_tickets_string}", f"Winning ticket: {winning_ticket[0]}", "YOU WIN"
            return f"Probability of winning: {probability}%", f"My tickets: {my_tickets_string}", f"Winning ticket: {winning_ticket[0]}", ""







if __name__ == "__main__":
    app.run_server(debug=True)
