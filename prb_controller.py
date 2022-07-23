import plotly.graph_objects as go
from dash import Input, Output, State, exceptions
from prb_view import app, blank_fig
import prb_model


def generate_graph(click_store, win_store, prob_store):
    fig = go.Figure()
    fig.update_layout(margin=dict(t=20, b=10, l=20, r=20),
                      height=300)
    fig.add_trace(go.Scatter(x=click_store,
                             y=win_store,
                             name="Observed wins",
                             marker_color="#d10373",
                             marker_opacity=0,
                             hovertemplate="Number of observed wins: %{y}<br>Number of draws: %{x}<extra></extra>"))
    fig.add_trace(go.Scatter(x=click_store,
                             y=prob_store,
                             name="Expected wins",
                             marker_color="#9eab05",
                             marker_opacity=0,
                             hovertemplate="Number of expected wins: %{y}<br>Number of draws: %{x}<extra></extra>"))
    return fig


@app.callback(
    Output("total-store", "data"),
    Output("num-store", "data"),
    Output("click-store", "data"),
    Output("prob-store", "data"),
    Output("win-store", "data"),
    Output("probability", "children"),
    Output("my-tickets", "children"),
    Output("winning-ticket", "children"),
    Output("win-rate", "children"),
    Output("draws", "children"),
    Output("graph", "figure"),
    Input("submit", "n_clicks"),
    State("total-tickets", "value"),
    State("num-tickets", "value"),
    State("total-store", "data"),
    State("num-store", "data"),
    State("click-store", "data"),
    State("win-store", "data"),
    State("prob-store", "data")
)
def update_stores(n_clicks, total, num, total_store, num_store, click_store, win_store, prob_store):
    if n_clicks is None:
        raise exceptions.PreventUpdate

    if num > total:
        return total_store, num_store, click_store, prob_store, win_store, "Tickets bought must be fewer than total tickets", "", "", "", "", blank_fig

    probability = round((num/total), 2)

    if total_store is None or num_store is None:
        total_store = total
        num_store = num
        click_store = [0]
        prob_store = [0]
        win_store = [0]
        return total_store, num_store, click_store, prob_store, win_store, f"Expected win rate: {str(int(probability*100))}%", "", "", "", "", blank_fig
    elif total != total_store or num != num_store:
        total_store = total
        num_store = num
        my_tickets, my_tickets_string, winning_ticket = prb_model.generate_tickets(
            total, num)
        click_store = [0, 1]
        prob_store = [0, probability]
        win_store = [0]
        winner = False
        for ticket in my_tickets:
            if ticket == winning_ticket:
                winner = True
        if winner == True:
            win_store.append(1)
            win_rate = round(win_store[-1]/click_store[-1], 2)
            fig = generate_graph(click_store, win_store, prob_store)
            return total_store, num_store, click_store, prob_store, win_store, f"Expected win rate: {str(int(probability*100))}%", f"My tickets: {my_tickets_string}", f"Winning ticket: {winning_ticket[0]} - WIN", f"Observed win rate: {str(int(win_rate*100))}%", f"Number of draws: {click_store[-1]}", fig
        else:
            win_store.append(0)
            win_rate = round(win_store[-1]/click_store[-1], 2)
            fig = generate_graph(click_store, win_store, prob_store)
            return total_store, num_store, click_store, prob_store, win_store, f"Expected win rate: {str(int(probability*100))}%", f"My tickets: {my_tickets_string}", f"Winning ticket: {winning_ticket[0]}", f"Observed win rate: {str(int(win_rate*100))}%", f"Number of draws: {click_store[-1]}", fig
    else:
        click_store.append(click_store[-1] + 1)
        prob_store.append(click_store[-1] * probability)
        my_tickets, my_tickets_string, winning_ticket = prb_model.generate_tickets(
            total, num)
        winner = False
        for ticket in my_tickets:
            if ticket == winning_ticket:
                winner = True
        if winner == True:
            win_store.append(win_store[-1] + 1)
            win_rate = round(win_store[-1]/click_store[-1], 2)
            fig = generate_graph(click_store, win_store, prob_store)
            return total_store, num_store, click_store, prob_store, win_store, f"Expected win rate: {str(int(probability*100))}%", f"My tickets: {my_tickets_string}", f"Winning ticket: {winning_ticket[0]} - WIN", f"Observed win rate: {str(int(win_rate*100))}%", f"Number of draws: {click_store[-1]}", fig
        else:
            win_store.append(win_store[-1])
            win_rate = round(win_store[-1]/click_store[-1], 2)
            fig = generate_graph(click_store, win_store, prob_store)
            return total_store, num_store, click_store, prob_store, win_store, f"Expected win rate: {str(int(probability*100))}%", f"My tickets: {my_tickets_string}", f"Winning ticket: {winning_ticket[0]}", f"Observed win rate: {str(int(win_rate*100))}%", f"Number of draws: {click_store[-1]}", fig


if __name__ == "__main__":
    app.run(debug=True)
