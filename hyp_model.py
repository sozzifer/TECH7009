import pandas as pd

df_rda = pd.read_csv("data/rda.csv").reset_index(drop=True)
df_age = pd.read_csv("data/age.csv").reset_index(drop=True)
df_antacid = pd.read_csv("data/antacid.csv").reset_index(drop=True)

rda = df_rda["rda"].tolist()
age = df_age["age"].tolist()
antacid = df_antacid["antacid"].tolist()
