import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.graphics.gofplots import qqplot
import plotly.graph_objects as go


df_quant = pd.read_csv("data/happy_quant.csv")


def not_null(x, y):
    not_empty = df_quant[(df_quant[x].notnull()) & (df_quant[y].notnull())]
    return not_empty


def regression(x, y):
    formula = f"{y} ~ {x}"
    model = ols(formula, data=df_quant)
    results = model.fit()
    summary = results.summary()
    params = results.params
    residuals = results.resid
    fitted = results.fittedvalues
    r_sq = results.rsquared
    return summary, params, residuals, fitted, r_sq


# https://www.statsmodels.org/dev/generated/statsmodels.regression.linear_model.OLS.html
model = ols("Weight ~ Height", data=df_quant)
results = model.fit()

# https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.RegressionResults.html
params = results.params
residuals = results.resid
fitted = results.fittedvalues
r_sq = results.rsquared
conf_int = results.conf_int(0.01)
# print(conf_int)
# print(results.summary())
# print(params)
# print(r_sq)


# Probability plot?
# qqplot_data = qqplot(residuals, line='s').gca().lines
# fig = go.Figure(go.Scatter(x=qqplot_data[0].get_xdata(),
#                            y=qqplot_data[0].get_ydata(),
#                            mode="markers"))
# fig.add_trace(go.Scatter(x=qqplot_data[1].get_xdata(),
#                          y=qqplot_data[1].get_ydata(),
#                          mode="lines"))
# fig.show()
