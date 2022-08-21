from dash import Dash, html, dcc, Input, Output, State, exceptions, no_update, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import scipy.stats as stat
from chi_view import app
from chi_model import calc_chi2_ind, stat_colours


@app.callback(
    Output("graph", "figure"),
    Output("sr-bar", "children"),
    Output("chi2", "children"),
    Output("p-value", "children"),
    Output("acc-rej-h0", "children"),
    Output("dependent", "invalid"),
    Input("dependent", "value"),
    Input("independent", "value")
)
def update_bar(dependent, independent):
    if dependent == independent:
        return no_update, no_update, no_update, no_update, no_update, True
    else:
        ct, ct_norm, ct_t, ct_table, dep_cat, ind_cat, chi2, p, dof, expected = calc_chi2_ind(
            dependent, independent)
        data = []
        for x in ct_t.columns:
            data.append(go.Bar(name=str(x),
                               x=ct_t.index,
                               y=ct_t[x],
                               marker_color=stat_colours[str(x)],
                               marker_opacity=0.7,
                               hovertemplate="Proportion: %{y:.2%}<extra></extra>"))
        fig = go.Figure(data)
        fig.update_layout(barmode="stack",
                          margin=dict(t=20, b=10, l=20, r=20),
                          height=400,
                          font_size=14,
                          legend_title_text=dependent,
                          legend_title_font_size=14,
                          xaxis_type="category")
        fig.update_xaxes(tick0=ct_t.index[0],
                         dtick=1,
                         title_text=independent)
        fig.update_yaxes(title_text=f"Proportion ({dependent})",
                         range=[0,1])
        sr_text = f"Bar chart of dependent variable {dependent} for independent variable {independent}"
        if p < 0.05:
            result = "Reject the null hypothesis"
        else:
            result = "Accept the null hypothesis"
    return fig, sr_text, f"{chi2:.3f}", f"{p:.3f}", result, False


def percent(x):
    return x*100


@app.callback(
    Output("table-observed", "children"),
    Output("table-expected", "children"),
    Output("table-observed-pc", "children"),
    Input("dependent", "value"),
    Input("independent", "value")
)
def update_datatables(dependent, independent):
    if dependent == independent:
        return no_update
    else:
        ct, ct_norm, ct_t, ct_table, dep_cat, ind_cat, chi2, p, dof, expected = calc_chi2_ind(
            dependent, independent)

        obs_df = ct.iloc[:-1, :]
        obs_df.rename(columns={"Expected": "Total"},
                      inplace=True)
        obs_df.sort_index(ascending=False, inplace=True)

        exp_df = pd.DataFrame(data=expected,
                              index=ct_table.columns,
                              columns=ct_table.index).round(2).iloc[:-1, :]
        exp_df.rename(columns={"Expected": "Total"},
                      inplace=True)
        exp_df.sort_index(ascending=False, inplace=True)

        obs_pc_df = ct_norm.applymap(percent).round(2)
        obs_pc_df.rename(columns={"UK": "UK (obs)",
                                  "EU": "EU (obs)",
                                  "International": "Int'l (obs)",
                                  "Y": "Y (obs)",
                                  "N": "N (obs)",
                                  "F": "F (obs)",
                                  "M": "M (obs)",
                                  "Extrovert": "Extrovert (obs)",
                                  "Introvert": "Introvert (obs)",
                                  "Expected": "Total (exp)"},
                         inplace=True)
        obs_pc_df.sort_index(ascending=False, inplace=True)

        table_observed = dash_table.DataTable(obs_df.to_dict("records"),
                                              [{"name": i, "id": i}
                                               for i in obs_df.columns],
                                              style_header={"fontWeight": "bold"},
                                              style_table={"width": "70%"},
                                              style_cell={"minWidth": "120px",
                                                          "width": "120px",
                                                          "maxWidth": "120px",
                                                          "font-family": "Regular"},
                                              fill_width=False,
                                              cell_selectable=False)
        table_expected = dash_table.DataTable(exp_df.to_dict("records"),
                                              [{"name": i, "id": i}
                                               for i in exp_df.columns],
                                              style_header={
                                                  "fontWeight": "bold"},
                                              style_table={"width": "70%"},
                                              style_cell={"minWidth": "120px",
                                                          "width": "120px",
                                                          "maxWidth": "120px",
                                                          "font-family": "Regular"},
                                              fill_width=False,
                                              cell_selectable=False)
        table_observed_pc = dash_table.DataTable(obs_pc_df.to_dict("records"),
                                                 [{"name": i, "id": i}
                                                  for i in obs_pc_df.columns],
                                                 style_header={
                                                     "fontWeight": "bold"},
                                                 style_table={"width": "70%"},
                                                 style_cell={"minWidth": "120px",
                                                             "width": "120px",
                                                             "maxWidth": "120px",
                                                             "font-family": "Regular"},
                                                 fill_width=False,
                                                 cell_selectable=False)
        return table_observed, table_expected, table_observed_pc
 

if __name__ == "__main__":
    app.run(debug=True)
