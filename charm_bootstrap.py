from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import pandas_datareader.data as web
import datetime

# start = datetime.datetime(2020, 1, 1)
# end = datetime.datetime(2020, 12, 3)
# df = web.DataReader(["AMZN", "GOOGL", "FB", "PFE", "BNTX", "MRNA"], data_source="stooq", start=start, end=end)
# # print(df.head())
# df = df.stack().reset_index()
# # print(df.head())
# df.to_csv("stocks.csv", index=False)

df = pd.read_csv("data/stocks.csv")

app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0"}]   # meta tags for mobile compatibility
           )

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Stock market dashboard",
                        className="text-center text-primary mb-4"),   # className to apply Bootstrap styles - no commas needed to assign multiple parameters
        width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id="dpdn1",
                         multi=False,
                         value="AMZN",
                         options=[{"label": x, "value": x}
                                  for x in sorted(df["Symbols"].unique())]),
            dcc.Graph(id="line-fig1", figure={})
        ], # width={"size": 5},   # Using dict allows for more flexibility in adjusting layout (size, order, offset)
           xs=12, sm=12, md=12, lg=5, xl=5),
        dbc.Col([
            dcc.Dropdown(id="dpdn2",
                         multi=True,
                         value=["PFE", "BNTX"],
                         options=[{"label": x, "value": x}
                                  for x in sorted(df["Symbols"].unique())]),
            dcc.Graph(id="line-fig2", figure={})
        ], # width={"size": 5},
           xs=12, sm=7, md=7, lg=5, xl=5)
    ], justify="start"),   # Check Row properties for more formatting options e.g. align
    dbc.Row([
        dbc.Col([
            html.P("Select company:",
                   style={"textDecoration": "underline"}),
            dcc.Checklist(id="checklist",
                          value=["FB", "GOOGL", "AMZN"],
                          options=[{"label": x, "value": x}
                                   for x in sorted(df["Symbols"].unique())],
                          labelClassName="m-2"),   # Utility-Spacing in Bootstrap m-x/p-x (margin/padding)
            dcc.Graph(id="hist-fig", figure={})
        ], # width={"size": 5},
           xs=12, sm=12, md=12, lg=5, xl=5),
        dbc.Col([
            dbc.Card([
                dbc.CardBody(
                    html.P("We're better together. Help each other out!",
                           className="card-text")
                ),
                dbc.CardImg(src="https://media.giphy.com/media/Ll0jnPa6IS8eI/giphy.gif",
                            bottom=True),
            ], style={"width": "24rem"})
        ], # width={"size": 5},
           xs=12, sm=12, md=12, lg=5, xl=5)
    ], align="center")
], fluid=True)   # dbc.Container fluid=True to use full width of page


@app.callback(
    Output('line-fig1', 'figure'),
    Input('dpdn1', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'] == stock_slctd]
    figln1 = px.line(dff, x='Date', y='High')
    return figln1


# Line chart - multiple
@app.callback(
    Output('line-fig2', 'figure'),
    Input('dpdn2', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    figln2 = px.line(dff, x='Date', y='Open', color='Symbols')
    return figln2


# Histogram
@app.callback(
    Output('hist-fig', 'figure'),
    Input('checklist', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    dff = dff[dff['Date'] == '2020-12-03']
    fighist = px.histogram(dff, x='Symbols', y='Close')
    return fighist


if __name__ == "__main__":
    app.run(debug=True)
