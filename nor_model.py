import plotly.graph_objects as go
import scipy.stats as stat
import numpy as np

stat_colours = {
    "norm": "#d10373",
    "z": "rgba(158, 171, 5, 0.5)",
    "mean": "#f49103",
    "+-1std": "#0085a1",
    "+-2std": "#003896",
    "+-3std": "#6a2150"
}


def create_blank_fig():
    x = np.linspace(stat.norm.ppf(0.0001),
                    stat.norm.ppf(0.9999),
                    10000)
    norm_x = stat.norm.pdf(x)
    blank_fig = go.Figure(
        go.Scatter(x=x, y=norm_x, marker_color=stat_colours["norm"]),
        layout={"margin": dict(t=20, b=10, l=20, r=20),
                "height": 400,
                "font_size": 14})
    return blank_fig

