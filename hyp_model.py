import pandas as pd
import scipy.stats as stat
import plotly.graph_objects as go
import numpy as np

df_rda = pd.read_csv("data/rda.csv").reset_index(drop=True)
df_age = pd.read_csv("data/age.csv").reset_index(drop=True)
df_antacid = pd.read_csv("data/antacid.csv").reset_index(drop=True)

rda = df_rda["rda"].tolist()
age = df_age["age"].tolist()
antacid = df_antacid["antacid"].tolist()

# k2, p = stat.normaltest(antacid)
# print(p)

# mean = np.mean(rda)
# std = np.std(rda)
# rda_cdf = stat.norm(mean, std).cdf(rda)
# rda_pdf = stat.norm(mean, std).pdf(rda)

# fig = go.Figure(go.Scatter(x=rda, y=rda_pdf, mode="markers"))
# fig.show()