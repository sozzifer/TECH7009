from dash import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from car_view import app
from car_model import not_null, regression
from statsmodels.formula.api import ols


@app.callback(
    Output("xy-graph", "figure"),
    Input("dropdown1", "value"),
    Input("dropdown2", "value")
)
def plot_x_y(x, y):
    df = not_null(x, y)
    fig = px.scatter(x=df[x],
                     y=df[y],
                     trendline="ols",
                     trendline_color_override="#d10373")
    fig.update_traces(marker_color="#9eab05", marker_size=4, line_width=3)
    fig.update_layout(margin=dict(t=20, b=10, l=20, r=20),
                      height=300,
                      font_size=14,
                      xaxis_title=x,
                      yaxis_title=y)
    return fig


@app.callback(
    Output("res-graph", "figure"),
    Output("results", "children"),
    Output("r-squared", "children"),
    Input("dropdown1", "value"),
    Input("dropdown2", "value")
)
def plot_res_v_fitted(x, y):
    summary, params, residuals, fitted, r_sq = regression(x, y)
    fig = go.Figure(
        go.Scatter(x=fitted,
                   y=residuals,
                   marker_color="#9eab05",
                   marker_size=4,
                   mode="markers",
                   showlegend=False))
    fig.update_layout(margin=dict(t=20, b=10, l=20, r=20),
                      height=300,
                      font_size=14,
                      xaxis_title="Fitted values",
                      yaxis_title="Residuals")
    zero_line = np.linspace(np.min(fitted), np.max(fitted), 100)
    fig.add_trace(go.Scatter(x=zero_line,
                             y=[0]*100,
                             line_width=3,
                             marker_color="#d10373",
                             showlegend=False))
    intercept = round(params[0], 3)
    slope = round(params[1], 3)
    if intercept < 0:
        equation = f"{slope} * {x} - {abs(intercept)}"
    else:
        equation = f"{slope} * {x} + {intercept}"
    return fig, equation, f"{r_sq:.3f}"


if __name__ == "__main__":
    app.run(debug=True)
