from dash import Dash, html, dcc, Input, Output, State, exceptions, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import scipy.stats as stat

df_quant = pd.read_csv("data/happy_quant.csv")
df_qual = pd.read_csv("data/happy_qual.csv")
qual_y_range = {"tothappy": 130,
                "height": 115,
                "weight": 80,
                "age": 400,
                "diff1": 310,
                "diff2": 310,
                "bmi": 80}


def get_df_qual(value):
    df = df_qual[value].dropna().reset_index(drop=True)
    categories = df.unique()
    x = ["Observed", "Expected"]
    y1 = df[(df == categories[0])].count()
    y2 = df[(df == categories[1])].count()
    expected_y = df.count()/2
    return x, y1, y2, expected_y, categories[0], categories[1]


def get_df_quant(value):
    df = df_quant[value].dropna().reset_index(drop=True)
    return df

