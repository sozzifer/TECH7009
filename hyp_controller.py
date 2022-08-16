from dash import Input, Output, State, exceptions, no_update
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
import scipy.stats as stat
from hyp_model import rda, age, antacid
from hyp_view import app

alt_dict = {"<": "less", ">": "greater", "!=": "two-sided"}


@app.callback(
    Output("graph", "figure"),
    Output("sr-hist", "children"),
    Output("conf-text", "children"),
    Output("conf-val", "children"),
    Output("results", "style"),
    Input("submit", "n_clicks"),
    State("dropdown", "value"),
    State("hyp-mean", "value"),
    State("alternative", "value"),
    State("alpha", "value"),
    prevent_initial_call=True
)
def update_histogram(n_clicks, dataset, hyp_mean, alternative, alpha):
    if n_clicks is None:
        raise exceptions.PreventUpdate
    else:
        fig = go.Figure(layout={"margin": dict(t=20, b=10, l=20, r=20),
                                "height": 400,
                                "font_size": 14})
        if dataset =="rda":
            fig.add_trace(go.Histogram(x=rda,
                                       xbins={"start": 5, "end": 21, "size": 2},
                                       name="Daily iron intake (mg)",
                                       marker_line_color="rgba(158,171,5,1)",
                                       marker_color="rgba(158,171,5,0.5)",
                                       marker_line_width=1))
            fig.update_xaxes(range=[5, 21])
            mean = np.mean(rda)
            sem = stat.sem(rda)
            nu = len(rda) - 1
            sr_text = "Histogram of iron intake for 45 randomly selected females aged under 51"
            if alternative == "<" or alternative == ">":
                conf_int = stat.t.interval(df=nu,
                                           alpha=alpha,
                                           loc=mean,
                                           scale=sem)
                if alternative == "<":
                    fig.add_trace(go.Scatter(x=np.linspace(5, conf_int[1], 100),
                                             y=[0.5]*100,
                                             name="Confidence interval",
                                             marker_color="#d10373"))
                    fig.add_trace(go.Scatter(x=[5],
                                             y=[0.5],
                                             marker_symbol="arrow-left",
                                             marker_color="#d10373",
                                             marker_size=14,
                                             showlegend=False)),
                    fig.add_trace(go.Scatter(x=[conf_int[1]],
                                             y=[0.5],
                                             mode="markers",
                                             marker_symbol="line-ns",
                                             marker_line_width=2,
                                             marker_line_color="#d10373",
                                             marker_size=12,
                                             showlegend=False)),
                    fig.add_trace(go.Scatter(x=[hyp_mean],
                                             y=[0.5],
                                             name="Hypothesised mean",
                                             mode="markers",
                                             marker_symbol="circle-x-open",
                                             marker_color="#d10373",
                                             marker_size=16))
                    conf_text = "Upper bound for population mean: "
                    conf_val = conf_int[1]
                elif alternative == ">":
                    fig.add_trace(go.Scatter(x=np.linspace(conf_int[0], 21, 100),
                                             y=[0.5]*100,
                                             name="Confidence interval",
                                             marker_color="#d10373"))
                    fig.add_trace(go.Scatter(x=[21],
                                             y=[0.5],
                                             marker_symbol="arrow-right",
                                             marker_color="#d10373",
                                             marker_size=14,
                                             showlegend=False)),
                    fig.add_trace(go.Scatter(x=[conf_int[0]],
                                             y=[0.5],
                                             mode="markers",
                                             marker_symbol="line-ns",
                                             marker_line_width=2,
                                             marker_line_color="#d10373",
                                             marker_size=12,
                                             showlegend=False)),
                    fig.add_trace(go.Scatter(x=[hyp_mean],
                                             y=[0.5],
                                             name="Hypothesised mean",
                                             mode="markers",
                                             marker_symbol="circle-x-open",
                                             marker_color="#d10373",
                                             marker_size=16))
                    conf_text = "Lower bound for population mean: "
                    conf_val = conf_int[0]
                return fig, sr_text, conf_text, f"{conf_val:.3f}", {"display": "inline"}
            else:
                conf_int = stat.t.interval(df=nu,
                                           alpha=(2*alpha)-1,
                                           loc=mean,
                                           scale=sem)
                fig.add_trace(go.Scatter(x=[conf_int[0], conf_int[1]],
                                         y=[0.5, 0.5],
                                         name="Confidence interval",
                                         mode="lines",
                                         marker_color="#d10373"))
                fig.add_trace(go.Scatter(x=[conf_int[0]],
                                         y=[0.5],
                                         mode="markers",
                                         marker_symbol="line-ns",
                                         marker_line_width=2,
                                         marker_line_color="#d10373",
                                         marker_size=12,
                                         showlegend=False)),
                fig.add_trace(go.Scatter(x=[conf_int[1]],
                                         y=[0.5],
                                         mode="markers",
                                         marker_symbol="line-ns",
                                         marker_line_width=2,
                                         marker_line_color="#d10373",
                                         marker_size=12,
                                         showlegend=False)),
                fig.add_trace(go.Scatter(x=[hyp_mean],
                                         y=[0.5],
                                         name="Hypothesised mean",
                                         mode="markers",
                                         marker_symbol="circle-x-open",
                                         marker_color="#d10373",
                                         marker_size=16))
                return fig, sr_text, "Confidence interval for population mean: ", f"({conf_int[0]:.3f}, {conf_int[1]:.3f})", {"display": "inline"}
        elif dataset == "age":
            fig.add_trace(go.Histogram(x=age,
                                       xbins={"start": 5, "end": 65, "size": 10},
                                       name="Age (years)",
                                       marker_line_color="rgba(158,171,5,1)",
                                       marker_color="rgba(158,171,5,0.5)",
                                       marker_line_width=1))
            fig.update_xaxes(range=[5, 65])
            sr_text = "Histogram of the ages of 10 randomly selected US citizens"
            return fig, sr_text, "", "", no_update
        elif dataset == "antacid":
            fig.add_trace(go.Histogram(x=antacid,
                                       xbins={"start": 3, "end": 17, "size": 2},
                                       name="Time to take effect (mins)",
                                       marker_line_color="rgba(158,171,5,1)",
                                       marker_color="rgba(158,171,5,0.5)",
                                       marker_line_width=1))
            fig.update_xaxes(range=[3, 17])
            mean = np.mean(antacid)
            sem = stat.sem(antacid)
            nu = len(antacid) - 1
            sr_text = "Histogram of times for relief for new antacid tablet"
            if alternative == "<" or alternative == ">":
                conf_int = stat.t.interval(df=nu,
                                           alpha=alpha,
                                           loc=mean,
                                           scale=sem)
                if alternative == "<":
                    fig.add_trace(go.Scatter(x=np.linspace(3, conf_int[1], 100),
                                             y=[0.5]*100,
                                             name="Confidence interval",
                                             marker_color="#d10373"))
                    fig.add_trace(go.Scatter(x=[3],
                                             y=[0.5],
                                             marker_symbol="arrow-left",
                                             marker_color="#d10373",
                                             marker_size=14,
                                             showlegend=False)),
                    fig.add_trace(go.Scatter(x=[conf_int[1]],
                                             y=[0.5],
                                             mode="markers",
                                             marker_symbol="line-ns",
                                             marker_line_width=2,
                                             marker_line_color="#d10373",
                                             marker_size=12,
                                             showlegend=False)),
                    fig.add_trace(go.Scatter(x=[hyp_mean],
                                             y=[0.5],
                                             name="Hypothesised mean",
                                             mode="markers",
                                             marker_symbol="circle-x-open",
                                             marker_color="#d10373",
                                             marker_size=16))
                    conf_text = f"Upper bound for population mean: "
                    conf_val = conf_int[1]
                elif alternative == ">":
                    fig.add_trace(go.Scatter(x=np.linspace(conf_int[0], 17, 100),
                                             y=[0.5]*100,
                                             name="Confidence interval",
                                             marker_color="#d10373"))
                    fig.add_trace(go.Scatter(x=[17],
                                             y=[0.5],
                                             marker_symbol="arrow-right",
                                             marker_color="#d10373",
                                             marker_size=14,
                                             showlegend=False)),
                    fig.add_trace(go.Scatter(x=[conf_int[0]],
                                             y=[0.5],
                                             mode="markers",
                                             marker_symbol="line-ns",
                                             marker_line_width=2,
                                             marker_line_color="#d10373",
                                             marker_size=12,
                                             showlegend=False)),
                    fig.add_trace(go.Scatter(x=[hyp_mean],
                                             y=[0.5],
                                             name="Hypothesised mean",
                                             mode="markers",
                                             marker_symbol="circle-x-open",
                                             marker_color="#d10373",
                                             marker_size=16))
                    conf_text = "Lower bound for population mean: "
                    conf_val = conf_int[0]
                return fig, sr_text, conf_text, f"{conf_val:.3f}", {"display": "inline"}
            else:
                conf_int = stat.t.interval(df=nu,
                                           alpha=(2*alpha)-1,
                                           loc=mean,
                                           scale=sem)
                fig.add_trace(go.Scatter(x=[conf_int[0], conf_int[1]],
                                         y=[0.5, 0.5],
                                         name="Confidence interval",
                                         mode="lines",
                                         marker_color="#d10373"))
                fig.add_trace(go.Scatter(x=[conf_int[0]],
                                         y=[0.5],
                                         mode="markers",
                                         marker_symbol="line-ns",
                                         marker_line_width=2,
                                         marker_line_color="#d10373",
                                         marker_size=12,
                                         showlegend=False)),
                fig.add_trace(go.Scatter(x=[conf_int[1]],
                                         y=[0.5],
                                         mode="markers",
                                         marker_symbol="line-ns",
                                         marker_line_width=2,
                                         marker_line_color="#d10373",
                                         marker_size=12,
                                         showlegend=False)),
                fig.add_trace(go.Scatter(x=[hyp_mean],
                                         y=[0.5],
                                         name="Hypothesised mean",
                                         mode="markers",
                                         marker_symbol="circle-x-open",
                                         marker_color="#d10373",
                                         marker_size=16))
                return fig, sr_text, "Confidence interval for population mean: ", f"({conf_int[0]:.3f}, {conf_int[1]:.3f})", {"display": "inline"}


@app.callback(
    Output("t-stat", "children"),
    Output("p-value", "children"),
    Output("acc-rej-h0", "children"),
    Input("submit", "n_clicks"),
    State("dropdown", "value"),
    State("hyp-mean", "value"),
    State("alternative", "value"),
    State("alpha", "value"),
    prevent_initial_call=True
)
def perform_t_test(n_clicks, dataset, hyp_mean, alternative, alpha):
    if n_clicks is None:
        raise exceptions.PreventUpdate
    else:
        alt = alt_dict[alternative]
        if dataset == "rda":
            t, p = stat.ttest_1samp(a=rda, popmean=hyp_mean, alternative=alt)
        elif dataset == "age":
            difference = [age - hyp_mean for age in age]
            t, p = stat.wilcoxon(x=difference, alternative=alt)
        elif dataset == "antacid":
            t, p = stat.ttest_1samp(a=antacid, popmean=hyp_mean, alternative=alt)
        if p < 1 - alpha:
            result = "Reject the null hypothesis"
        else:
            result = "Accept the null hypothesis"
        return f"{t: .3f}", f"{p: g}", result


@app.callback(
    Output("hyp-mean", "min"),
    Output("hyp-mean", "max"),
    Output("hyp-mean", "placeholder"),
    Output("hyp-mean", "value"),
    Input("dropdown", "value")
)
def set_hyp_min_max(dataset):
    if dataset == "age":
        hyp_min = 5
        hyp_max = 65
    elif dataset == "antacid":
        hyp_min = 3
        hyp_max = 17
    elif dataset == "rda":
        hyp_min = 5
        hyp_max = 21
    hyp_label = f"Enter a value between {hyp_min} and {hyp_max}"
    return hyp_min, hyp_max, hyp_label, None

if __name__ == "__main__":
    app.run(debug=True)
