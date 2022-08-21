from dash import Input, Output, State, exceptions, no_update
import plotly.graph_objects as go
import scipy.stats as stat
from tsh_view import app
from tsh_model import get_df

alt_dict = {"<": "less", ">": "greater", "!=": "two-sided"}


def format_histogram(df, fig):
    fig.update_layout(margin=dict(t=20, b=10, l=20, r=20),
                      height=300,
                      font_size=14)
    fig.update_xaxes(range=[0, 28.5],
                     dtick=7,
                     tick0=7)
    fig.update_yaxes(title_text=None,
                     range=[0, 91])
    fig.update_traces(marker_line_width=1)


def hist_hovertext(df):
    sum = df.value_counts().sum()
    proportions = []
    for value in df.value_counts():
        proportions.append(round((value/sum)*100, 2))
    return proportions


@app.callback(
    Output("graph-hist1", "figure"),
    Output("graph-hist2", "figure"),
    Output("sr-hist1", "children"),
    Output("sr-hist2", "children"),
    Input("cols-dropdown", "value")
)
def update_histogram(value):
    categories, hist_df1, hist_df2 = get_df(value)

    fig1 = go.Figure(
        go.Histogram(x=hist_df1,
                     xaxis="x2",
                     customdata=hist_hovertext(hist_df1),
                     hovertemplate="Total happiness score: %{x}" + "<br>Count: %{y}" +
                     "<br>Proportion: %{customdata}%<extra></extra>",
                     showlegend=False),
    )
    fig2 = go.Figure(
        go.Histogram(x=hist_df2,
                     xaxis="x2",
                     customdata=hist_hovertext(hist_df2),
                     hovertemplate="Total happiness score: %{x}" + "<br>Count: %{y}" +
                     "<br>Proportion: %{customdata}%<extra></extra>",
                     showlegend=False)
    )
    fig1.update_traces(marker_line_color="rgba(209,3,115,1)",
                       marker_color="rgba(209,3,115,0.5)")
    fig1.update_xaxes(
        title_text=f"Histogram of Total happiness for {value} = {categories[0]}")
    fig2.update_traces(marker_line_color="rgba(158,171,5,1)",
                       marker_color="rgba(158,171,5,0.5)")
    fig2.update_xaxes(
        title_text=f"Histogram of Total happiness for {value} = {categories[1]}")
    format_histogram(hist_df1, fig1)
    format_histogram(hist_df2, fig2)

    sr_hist1 = f"Histogram of Total happiness for {value} = {categories[0]}"
    sr_hist2 = f"Histogram of Total happiness for {value} = {categories[1]}"

    return fig1, fig2, sr_hist1, sr_hist2


@app.callback(
    Output("t-stat", "children"),
    Output("p-value", "children"),
    Output("acc-rej-h0", "children"),
    Output("results", "style"),
    Input("submit", "n_clicks"),
    State("cols-dropdown", "value"),
    State("alternative", "value"),
    prevent_initial_call=True
)
def update_results(n_clicks, value, alternative):
    if n_clicks is None:
        raise exceptions.PreventUpdate
    else:
        alt = alt_dict[alternative]
        categories, df1, df2 = get_df(value)
        t, p = stat.ttest_ind(df1, df2, alternative=alt)
        if p < 0.05:
            result = "Reject the null hypothesis"
        else:
            result = "Accept the null hypothesis"
    return f"{t: .3f}", f"{p: g}", result, {"display": "inline"}



if __name__ == "__main__":
    app.run(debug=True)
