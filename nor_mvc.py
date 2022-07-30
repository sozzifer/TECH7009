from dash import Dash, html, dcc, Input, Output, State, exceptions, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import scipy.stats as stat

app = Dash(__name__,
           title="Normal distribution",
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width,\
                                   initial-scale=1.0,\
                                   maximum-scale=1.0"
           }]
)

app.layout = dbc.Container([
    dbc.Row([
        html.H1("Normal distribution")
    ], style={"padding": 20}),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="normal-dist-fig", style={"height": 300})
        ], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([
            html.P("Z calculation here")
        ], id="z-output", xs=12, sm=12, md=12, lg=6, xl=6, style={"display": "none"})
    ]),
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Label("Mean: "),
            html.Br(),
            dcc.Input(id="mu",
                      value=0,
                      type="number"),
            html.Br(),
            html.Br(),
            html.Label("Standard deviation: "),
            html.Br(),
            dcc.Input(id="sigma",
                      value=1,
                      type="number"),
            html.Br(),
            html.Br(),
            html.Button(id="submit",
                        n_clicks=0,
                        children="Submit")
        ]),
        dbc.Col([
            html.Br(),
            html.Label("Calculation type: "),
            html.Br(),
            dcc.Dropdown(id="calc-type", options=[{"label": "< (less than)", "value": "<"}, {
                         "label": "> (greater than)", "value": ">"}, {"label": "= (equal to)", "value": "="}], value=None),
            html.Br(),
            html.Label("Z value: "),
            html.Br(),
            dcc.Input(id="z-value", type="number", value=None)
        ], id="z-input", style={"display": "none"})
    ]),
    dbc.Row(id="data-table", children=[])
])


@app.callback(
    Output("normal-dist-fig", "figure"),
    Output("z-input", "style"),
    Output("data-table", "children"),
    Input("submit", "n_clicks"),
    State("mu", "value"),
    State("sigma", "value"),
)
def generate_normal_dist(n_clicks, mu, sigma):
    if not n_clicks:
        raise exceptions.PreventUpdate
    else:
        df = pd.DataFrame({"x_range": np.linspace(stat.norm(loc=mu, scale=sigma).ppf(
            0.0001), stat.norm(loc=mu, scale=sigma).ppf(0.9999), 10000)})
        df["norm_x"] = stat.norm(loc=mu, scale=sigma).pdf(df["x_range"])
        df["z_score"] = stat.zscore(df["x_range"])
        df_dict=df.to_dict("records")
        print(df["x_range"].mean())
        print(df["x_range"].std())
        # print(df["norm_x"])
        # print(df["z_score"])

        fig1 = px.scatter(x=df["x_range"], y=df["norm_x"])
    return fig1, {"display": "inline"}, html.Div([
        dash_table.DataTable(data=df_dict,
                             columns=[{"name": i, "id": i}
                                      for i in df.columns],
                             export_format="csv")
    ])


@app.callback(
    Output("z-output", "style"),
    Input("calc-type", "value"),
    Input("z-value", "value")
)
def z_calculation(calc_type, z):
    if calc_type is None or z is None:
        raise exceptions.PreventUpdate
    else:
        return {"display": "inline"}


if __name__ == "__main__":
    app.run_server(debug=True)
