from dash import Input, Output, State
import plotly.express as px
from dis_view import app
import dis_model


@app.callback(
    Output("category1", "children"),
    Output("category2", "children"),
    Output("group1", "children"),
    Output("group2", "children"),
    Output("n1", "children"),
    Output("n2", "children"),
    Output("mean1", "children"),
    Output("std1", "children"),
    Output("q1_1", "children"),
    Output("median1", "children"),
    Output("q3_1", "children"),
    Output("iqr1", "children"),
    Output("mean2", "children"),
    Output("std2", "children"),
    Output("q1_2", "children"),
    Output("median2", "children"),
    Output("q3_2", "children"),
    Output("iqr2", "children"),
    Input("cols-dropdown", "value")
)
def update_statistics(value):
    categories, stats_df1, stats_df2 = dis_model.get_df(value)
    n1, mean1, std1, q1_1, median1, q3_1, iqr1 = dis_model.get_stats(stats_df1)
    n2, mean2, std2, q1_2, median2, q3_2, iqr2 = dis_model.get_stats(stats_df2)

    group1 = categories[0]
    group2 = categories[1]
    return f"{value}:", f"{value}:", group1, group2, n1, n2, mean1, u"\u00B1"+ str(std1), q1_1, median1, q3_1, iqr1, mean2, u"\u00B1" + str(std2), q1_2, median2, q3_2, iqr2


def format_histogram(df, fig):
    fig.update_layout(margin=dict(t=10, b=10), modebar_remove=["autoscale","pan", "lasso", "select", "zoom", "zoomin", "zoomout", "resetscale", "toimage"])
    fig.update_xaxes(range=[0, 28.5],
                     dtick=7,
                     tick0=7)
    fig.update_yaxes(title_text=None,
                     range=[0, 91])
    fig.add_vline(x=df.mean(),
                  line_color="#f49103")
    fig.add_vline(x=df.median(),
                  line_color="#006338")
    fig.add_vline(x=df.mean() + df.std(),
                  line_color="#0085a1")
    fig.add_vline(x=df.mean() - df.std(),
                  line_color="#0085a1")
    fig.add_vline(x=df.quantile(0.25),
                  line_color="#c70540")
    fig.add_vline(x=df.quantile(0.75),
                  line_color="#c70540")


@app.callback(
    Output("output-hist1", "figure"),
    Output("output-hist2", "figure"),
    Input("cols-dropdown", "value")
)
def update_histogram(value):
    categories, hist_df1, hist_df2 = dis_model.get_df(value)
    fig1 = px.histogram(
        hist_df1,
        x="Total happiness",
        height=300)
    fig2 = px.histogram(
        hist_df2,
        x="Total happiness",
        height=300)
    fig1.update_traces(
        marker_line_width=1,
        marker_line_color="rgba(209,3,115,1)",
        marker_color="rgba(209,3,115,0.5)")
    fig1.update_xaxes(
        title_text=f"Histogram of Total happiness for {categories[0]}")
    fig2.update_traces(
        marker_line_width=1,
        marker_line_color="rgba(158,171,5,1)",
        marker_color="rgba(158,171,5,0.5)")
    fig2.update_xaxes(
        title_text=f"Histogram of Total happiness for {categories[1]}")
    format_histogram(hist_df1, fig1)
    format_histogram(hist_df2, fig2)

    return fig1, fig2


def format_boxplot(df, fig):
    fig.update_layout(margin=dict(t=10, b=10), modebar_remove=[
                      "autoscale", "pan", "lasso", "select", "zoom", "zoomin", "zoomout", "resetscale", "toimage"])
    fig.update_traces(hoveron="boxes")
    fig.update_xaxes(range=[0, 28.5],
                     dtick=7,
                     tick0=7)
    fig.update_yaxes(visible=False,
                     showticklabels=False)
    fig.add_vline(x=df.mean(),
                  line_color="#f49103")
    fig.add_vline(x=df.median(),
                  line_color="#006338")
    fig.add_vline(x=df.mean() + df.std(),
                  line_color="#0085a1")
    fig.add_vline(x=df.mean() - df.std(),
                  line_color="#0085a1")
    fig.add_vline(x=df.quantile(0.25),
                  line_color="#c70540")
    fig.add_vline(x=df.quantile(0.75),
                  line_color="#c70540")


@app.callback(
    Output("output-box1", "figure"),
    Output("output-box2", "figure"),
    Input("cols-dropdown", "value")
)
def update_boxplot(value):
    categories, box_df1, box_df2 = dis_model.get_df(value)
    fig1 = px.box(
        box_df1,
        orientation="h",
        height=250)
    fig2 = px.box(
        box_df2,
        orientation="h",
        height=250)
    fig1.update_traces(marker_color="#d10373")
    fig2.update_traces(marker_color="#9eab05")
    fig1.update_xaxes(
        title_text=f"Boxplot of Total happiness for {categories[0]}")
    fig2.update_xaxes(
        title_text=f"Boxplot of Total happiness for {categories[1]}")
    format_boxplot(box_df1, fig1)
    format_boxplot(box_df2, fig2)

    return fig1, fig2


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
    app.run_server(debug=True)
