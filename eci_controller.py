from dash import Input, Output
import plotly.graph_objects as go
import numpy as np
import scipy.stats as stat
import statsmodels.stats.proportion as statmod
from eci_view import app
from eci_model import get_df_qual, get_df_quant, df_qual, qual_y_range


@app.callback(
    Output("quant-hist", "figure"),
    Output("quant-variable", "children"),
    Output("quant-mean", "children"),
    Output("quant-conf-int", "children"),
    Output("quant-conf-level", "children"),
    Output("sr-hist", "children"),
    Input("quant-dropdown", "value"),
    Input("quant-conf-value", "value")
)
def update_histogram(value, conf_level):
    df = get_df_quant(value)
    fig = go.Figure(
        go.Histogram(x=df,
                     showlegend=False))
    fig.update_traces(marker_line_color="rgba(158,171,5,1)",
                      marker_color="rgba(158,171,5,0.5)",
                      marker_line_width=1)
    fig.update_yaxes(title_text=None,
                     range=[0, qual_y_range[value]])
    fig.update_layout(margin=dict(t=20, b=10, l=20, r=20))
    mean = np.mean(df)
    sem = stat.sem(df)
    conf_int = stat.norm.interval(
        alpha=conf_level,
        loc=mean,
        scale=sem)
    round_mean = round(mean, 3)
    ci_lower = round(conf_int[0], 3)
    ci_upper = round(conf_int[1], 3)
    conf_percent = conf_level*100
    add_ci_lines(fig, value, ci_lower, ci_upper)
    sr_hist = f"Histogram of {value} with confidence interval ({ci_lower}, {ci_upper})"
    return fig, f"Variable: {value}", f"Sample mean: {round_mean}", f"Confidence interval for the mean: ({ci_lower}, {ci_upper})", f"Confidence level: {conf_percent}%", sr_hist


def add_ci_lines(fig, value, ci_lower, ci_upper):
    y = np.linspace(0, qual_y_range[value], 10)
    fig.add_trace(
        go.Scatter(x=[ci_lower] * 10,
                   y=y,
                   marker_opacity=0,
                   marker_color="#0085a1",
                   name="CI lower bound")
    )
    fig.add_trace(
        go.Scatter(x=[ci_upper] * 10,
                   y=y,
                   marker_opacity=0,
                   marker_color="#0085a1",
                   name="CI upper bound")
    )
    return fig


@app.callback(
    Output("cat-radio", "options"),
    Output("cat-radio", "value"),
    Input("qual-dropdown", "value")
)
def set_categories(value):
    df = df_qual[value]
    categories = df.unique()
    cat1 = categories[0]
    cat2 = categories[1]
    return [{"label": cat1, "value": cat1}, {"label": cat2, "value": cat2}], cat1


@app.callback(
    Output("qual-bar", "figure"),
    Output("qual-proportion1", "children"),
    Output("qual-proportion2", "children"),
    Output("qual-population", "children"),
    Output("qual-conf-int", "children"),
    Output("qual-conf-level", "children"),
    Output("sr-bar", "children"),
    Input("qual-dropdown", "value"),
    Input("qual-conf-value", "value"),
    Input("cat-radio", "value")
)
def update_bar(value, conf_level, category):
    x, y1, y2, expected_y, cat1, cat2 = get_df_qual(value, category)
    y1_val = [y1, expected_y]
    y2_val = [y2, expected_y]
    conf_percent = conf_level*100
    fig = go.Figure(data=[go.Bar(name=cat1,
                                 x=x,
                                 y=y1_val,
                                 marker_color="#d10373",
                                 marker_opacity=0.6),
                          go.Bar(name=cat2,
                                 x=x,
                                 y=y2_val,
                                 marker_color="#9eab05",
                                 marker_opacity=0.6)])
    fig.update_layout(barmode="stack",
                      margin=dict(t=20, b=10, l=20, r=20))
    fig.update_yaxes(title_text=None,
                     range=[0, (y1+y2)+1])
    x = y1
    n = y1 + y2
    conf_int = statmod.proportion_confint(x, n, 1-conf_level, "normal")
    ci_lower = round(conf_int[0]*n, 2)
    ci_upper = round(conf_int[1]*n, 2)
    fig.add_shape(type="line",
                  xref="paper",
                  yref="paper",
                  x0=0,
                  y0=conf_int[0],
                  x1=1,
                  y1=conf_int[0],
                  line=dict(color="#0085a1",
                            width=2))
    fig.add_shape(type="line",
                  xref="paper",
                  yref="paper",
                  x0=0,
                  y0=conf_int[1],
                  x1=1,
                  y1=conf_int[1],
                  line=dict(color="#0085a1",
                            width=2))
    sr_bar = f"Barchart of {value} with confidence interval for {cat1} ({ci_lower}, {ci_upper}"
    return fig, f"Count of {cat1}: {y1}", f"Count of {cat2}: {y2}", f"Total count: {n}", f"Confidence interval for {cat1}: ({ci_lower}, {ci_upper})", f"Confidence level: {conf_percent}%", sr_bar


if __name__ == "__main__":
    app.run(debug=True)
