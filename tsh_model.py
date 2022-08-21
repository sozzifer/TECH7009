import pandas as pd

happy_df = pd.read_csv("data/dis_happy.csv")

def get_df(value):
    df = happy_df[["Total happiness", value]].dropna().reset_index(drop=True)
    categories = df[value].unique()
    df1 = df["Total happiness"][(df[value] == categories[0])]
    df2 = df["Total happiness"][(df[value] == categories[1])]
    return categories, df1, df2






# def welch_ttest(df1, df2):
#     m1 = np.mean(df1)
#     m2 = np.mean(df2)
#     v1 = np.var(df1)
#     v2 = np.var(df2)
#     n1 = df1.size
#     n2 = df2.size
#     pooled_se = np.sqrt(v1/n1 + v2/n2)
#     delta = m1-m2
#     t = delta/pooled_se
#     nu = ((v1/n1 + v2/n2)**2)/(((v1/n1)**2/(n1-1))+((v2/n2)**2/(n2-1)))
#     p = 2 * stat.t.cdf(-abs(t), nu)
#     lb = delta - stat.t.ppf(0.975, nu)*pooled_se
#     ub = delta + stat.t.ppf(0.975, nu)*pooled_se
#     return pd.DataFrame(np.array([t, nu, p, delta, lb, ub]).reshape(1, -1),
#                        columns=['T statistic', 'df', 'pvalue 2 sided', 'Difference in mean', 'lb', 'ub'])

# t_crit_1sided = {1164: {0.9: 1.282279,
#                         0.95: 1.646164,
#                         0.975: 1.962004,
#                         0.99: 2.329556,
#                         0.995: 2.58006},
#                  1168: {0.9: 1.282277,
#                         0.95: 1.646159,
#                         0.975: 1.961997,
#                         0.99: 2.329545,
#                         0.995: 2.580045},
#                  1126: {0.9: 1.282304,
#                         0.95: 1.646208,
#                         0.975: 1.962073,
#                         0.99: 2.329664,
#                         0.995: 2.580203},
#                  1148: {0.9: 1.282289,
#                         0.95: 1.646182,
#                         0.975: 1.962033,
#                         0.99: 2.329601,
#                         0.995: 2.580119}}
# t_crit_2sided = {1164: {0.9: 1.646164,
#                         0.95: 1.962004,
#                         0.975: 2.244306,
#                         0.99: 2.58006,
#                         0.995: 2.812397},
#                  1168: {0.9: 1.646159,
#                         0.95: 1.961997,
#                         0.975: 2.244296,
#                         0.99: 2.580045,
#                         0.995: 2.812378},
#                  1126: {0.9: 1.646208,
#                         0.95: 1.962073,
#                         0.975: 2.244404,
#                         0.99: 2.580203,
#                         0.995: 2.812578},
#                  1148: {0.9: 1.646182,
#                         0.95: 1.962033,
#                         0.975: 2.244347,
#                         0.99: 2.580119,
#                         0.995: 2.812471}}

# nu_dict = {"Sex": 1168, "UK": 1168, "Extrovert_introvert": 1126, "Bored": 1164, "Absorbed": 1148}
# alpha = 0.975
# mean1 = np.mean(df1)
# mean2 = np.mean(df2)
# var1 = np.var(df1)
# var2 = np.var(df2)
# n1 = df1.size
# n2 = df2.size
# upper_ci = (mean1 - mean2) + \
#     t_crit_1sided[nu_dict["Sex"]][alpha]*math.sqrt((var1/n1)+(var2/n2))
# lower_ci = (mean1 - mean2) - \
#     t_crit_1sided[nu_dict["Sex"]][alpha]*math.sqrt((var1/n1)+(var2/n2))
# print(lower_ci)
# print(upper_ci)