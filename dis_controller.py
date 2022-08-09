from dash import html, Input, Output, State
import plotly.express as px
from dis_view import app
import dis_model
import plotly.graph_objects as go
import numpy as np

stat_colours = {
    "grp1": "#d10373",
    "grp2": "#9eab05",
    "mean": "#f49103",
    "median": "#006338",
    "std": "#0085a1",
    "quartile": "#c70540"
}


@app.callback(
    Output("desc1", "children"),
    Output("desc2", "children"),
    Input("cols-dropdown", "value")
)
def update_statistics(value):
    categories, stats_df1, stats_df2 = dis_model.get_df(value)
    group1 = categories[0]
    group2 = categories[1]
    n1, mean1, std1, q1_1, median1, q3_1, iqr1 = dis_model.get_stats(stats_df1)
    n2, mean2, std2, q1_2, median2, q3_2, iqr2 = dis_model.get_stats(stats_df2)
    f_std1 = u"\u00B1" + str(std1)
    f_std2 = u"\u00B1" + str(std2)
    return [html.Thead([html.Th(children=[f"{value}"], className="right"),
                        html.Th(children=[f"{group1}"]),
                        html.Th(children=["Key"])]),
            html.Tr([html.Td(children=["Sample size:"], className="right"),
                     html.Td(children=[f"{n1}"])]),
            html.Td(children=[]),
            html.Tr([html.Td(children=["Mean:"], className="right"),
                     html.Td(children=[f"{mean1}"]),
                     html.Td(html.Span(className="mean-key"))]),
            html.Tr([html.Td(children=["Median:"], className="right"),
                     html.Td(children=[f"{median1}"]),
                     html.Td(html.Span(className="median-key"))]),
            html.Tr([html.Td(children=["Standard deviation:"], className="right"),
                     html.Td(children=[f_std1]),
                     html.Td(html.Span(className="std-key"))]),
            html.Tr([html.Td(children=["First quartile (Q1):"], className="right"),
                     html.Td(children=[f"{q1_1}"]),
                     html.Td(html.Span(className="q1-key"))]),
            html.Tr([html.Td(children=["Third quartile (Q3):"], className="right"),
                     html.Td(children=[f"{q3_1}"]),
                     html.Td(html.Span(className="q3-key"))]),
            html.Tr([html.Td(children=["Interquartile range:"], className="right"),
                     html.Td(children=[f"{iqr1}"]),
                     html.Td(children=[])])],\
        [html.Thead([html.Th(children=[f"{value}"], className="right"),
                     html.Th(children=[f"{group2}"]),
                     html.Th(children=["Key"])]),
         html.Tr([html.Td(children=["Sample size:"], className="right"),
                  html.Td(children=[f"{n2}"])]),
         html.Td(children=[]),
         html.Tr([html.Td(children=["Mean:"], className="right"),
                  html.Td(children=[f"{mean2}"]),
                  html.Td(html.Span(className="mean-key"))]),
         html.Tr([html.Td(children=["Median:"], className="right"),
                  html.Td(children=[f"{median2}"]),
                  html.Td(html.Span(className="median-key"))]),
         html.Tr([html.Td(children=["Standard deviation:"], className="right"),
                  html.Td(children=[f_std2]),
                  html.Td(html.Span(className="std-key"))]),
         html.Tr([html.Td(children=["First quartile (Q1):"], className="right"),
                  html.Td(children=[f"{q1_2}"]),
                  html.Td(html.Span(className="q1-key"))]),
         html.Tr([html.Td(children=["Third quartile (Q3):"], className="right"),
                  html.Td(children=[f"{q3_2}"]),
                  html.Td(html.Span(className="q3-key"))]),
         html.Tr([html.Td(children=["Interquartile range:"], className="right"),
                  html.Td(children=[f"{iqr2}"]),
                  html.Td(children=[])])]


def format_histogram(df, fig):
    scatter_range = list(range(0, 93))
    _, mean, std, q1, median, q3, _ = dis_model.get_stats(df)

    fig.update_layout(xaxis2=dict(matches='x',
                                  layer="above traces",
                                  overlaying="x"),
                      margin=dict(t=10, b=20),
                      height=300,
                      xaxis={"side": "top"})
    fig.update_xaxes(range=[0, 28.5],
                     dtick=7,
                     tick0=7)
    fig.update_yaxes(title_text=None,
                     range=[0, 91])
    fig.update_traces(marker_line_width=1)
    fig.add_trace(
        go.Scatter(x=[mean] * 92,
                   y=scatter_range,
                   marker_color=stat_colours["mean"],
                   hovertemplate="Mean: %{x:.3f}<extra></extra>",
                   showlegend=False)
    )
    fig.add_trace(
        go.Scatter(x=[median] * 92,
                   y=scatter_range,
                   marker_color=stat_colours["median"],
                   hovertemplate="Median: %{x}<extra></extra>",
                   showlegend=False)
    )
    fig.add_trace(
        go.Scatter(x=[mean + std] * 92,
                   y=scatter_range,
                   marker_color=stat_colours["std"],
                   hovertemplate="Mean + SD: %{x:.3f}<extra></extra>",
                   showlegend=False)
    )
    fig.add_trace(
        go.Scatter(x=[mean - std] * 92,
                   y=scatter_range,
                   marker_color=stat_colours["std"],
                   hovertemplate="Mean - SD: %{x:.3f}<extra></extra>",
                   showlegend=False)
    )
    fig.add_trace(
        go.Scatter(x=[q1] * 92,
                   y=scatter_range,
                   marker_color=stat_colours["quartile"],
                   hovertemplate="Q1: %{x}<extra></extra>",
                   showlegend=False)
    )
    fig.add_trace(
        go.Scatter(x=[q3] * 92,
                   y=scatter_range,
                   marker_color=stat_colours["quartile"],
                   hovertemplate="Q3: %{x}<extra></extra>",
                   showlegend=False)
    )


def hist_hovertext(df):
    sum = df.value_counts().sum()
    proportions = []
    for value in df.value_counts():
        proportions.append(round((value/sum)*100, 2))
    return proportions


@app.callback(
    Output("graph-hist1", "figure"),
    Output("graph-hist2", "figure"),
    Input("cols-dropdown", "value")
)
def update_histogram(value):
    categories, hist_df1, hist_df2 = dis_model.get_df(value)

    fig1 = go.Figure(
        go.Histogram(x=hist_df1,
                     xaxis="x2",
                     customdata=hist_hovertext(hist_df1),
                     hovertemplate="Total happiness score: %{x}" + "<br>Count: %{y}" +
                     "<br>Proportion: %{customdata}%<extra></extra>",
                     showlegend=False)
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

    return fig1, fig2


def format_boxplot(df, fig, color):
    scatter_range = np.linspace(-0.5, 0.5, 100)
    _, mean, std, q1, median, q3, _ = dis_model.get_stats(df)

    fig.add_trace(
        go.Scatter(x=[mean]*100,
                   y=scatter_range,
                   marker_opacity=0,
                   marker_color=stat_colours["mean"],
                   hovertemplate="Mean: %{x}<extra></extra>",
                   showlegend=False)
    )
    fig.add_trace(
        go.Scatter(x=[median]*100,
                   y=scatter_range,
                   marker_opacity=0,
                   marker_color=stat_colours["median"],
                   hovertemplate="Median: %{x}<extra></extra>",
                   showlegend=False)
    )
    fig.add_trace(
        go.Scatter(x=[mean + std]*100,
                   y=scatter_range,
                   marker_opacity=0,
                   marker_color=stat_colours["std"],
                   hovertemplate="Mean + SD: %{x:.3f}<extra></extra>",
                   showlegend=False)
    )
    fig.add_trace(
        go.Scatter(x=[mean - std]*100,
                   y=scatter_range,
                   marker_opacity=0,
                   marker_color=stat_colours["std"],
                   hovertemplate="Mean - SD: %{x:.3f}<extra></extra>",
                   showlegend=False)
    )
    fig.add_trace(
        go.Scatter(x=[q1]*100,
                   y=scatter_range,
                   marker_opacity=0,
                   marker_color=stat_colours["quartile"],
                   hovertemplate="Q1: %{x}<extra></extra>",
                   showlegend=False)
    )
    fig.add_trace(
        go.Scatter(x=[q3]*100,
                   y=scatter_range,
                   marker_opacity=0,
                   marker_color=stat_colours["quartile"],
                   hovertemplate="Q3: %{x}<extra></extra>",
                   showlegend=False)
    )
    fig.add_trace(
        go.Box(x=df,
               xaxis="x2",
               hoverinfo="skip",
               hovertemplate=None,
               showlegend=False,
               marker_color=color)
    )
    fig.update_layout(xaxis2=dict(matches='x',
                                  layer="above traces",
                                  overlaying="x"),
                      margin=dict(t=10, b=10),
                      height=300,
                      xaxis={"side": "top"})
    fig.update_xaxes(range=[0, 28.5],
                     dtick=7,
                     tick0=7)
    fig.update_yaxes(visible=False,
                     showticklabels=False,
                     range=[-0.5, 0.5])
    return fig


@app.callback(
    Output("graph-box1", "figure"),
    Output("graph-box2", "figure"),
    Input("cols-dropdown", "value")
)
def update_boxplot(value):
    categories, box_df1, box_df2 = dis_model.get_df(value)
    fig1 = go.Figure()
    fig2 = go.Figure()
    fig1.update_xaxes(
        title_text=f"Boxplot of Total happiness for {value} = {categories[0]}")
    fig2.update_xaxes(
        title_text=f"Boxplot of Total happiness for {value} = {categories[1]}")
    format_boxplot(box_df1, fig1, stat_colours["grp1"])
    format_boxplot(box_df2, fig2, stat_colours["grp2"])
    return fig1, fig2


@app.callback(
    Output("sr-hist1", "children"),
    Output("sr-hist2", "children"),
    Output("sr-box1", "children"),
    Output("sr-box2", "children"),
    Input("cols-dropdown", "value")
)
def graph_alt_text(value):
    categories, _, _ = dis_model.get_df(value)
    sr_hist1 = f"Histogram of Total happiness for {value} = {categories[0]}"
    sr_hist2 = f"Histogram of Total happiness for {value} = {categories[1]}"
    sr_box1 = f"Boxplot of Total happiness for {value} = {categories[0]}"
    sr_box2 = f"Boxplot of Total happiness for {value} = {categories[1]}"
    return sr_hist1, sr_hist2, sr_box1, sr_box2


@app.callback(
    Output("collapse1", "is_open"),
    Output("collapse2", "is_open"),
    Input("toggle", "n_clicks"),
    State("collapse1", "is_open"),
    State("collapse2", "is_open"),
)
def toggle(n_clicks, is_open1, is_open2):
    if n_clicks:
        return not is_open1, not is_open2
    return is_open1, is_open2


if __name__ == "__main__":
    app.run(debug=True)
