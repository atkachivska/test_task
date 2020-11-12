import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def str_to_date(string):
    try:
        return datetime.datetime.fromisoformat(string)
    except:
        return string
    
def minus_month(x):
    try:
        return datetime.datetime(x.year, (x - datetime.timedelta(days=31)).month, x.day)
    except:
        return None
    
def plot_barplot(df, x, y, size = (18,6)):
    fig, ax = plt.subplots(figsize=size)
    plt.xticks(rotation=70)
    chart = sns.barplot(x = x, y = y,  data = df, color = 'lightgreen')
    chart.axhline(int(df.amount.mean()))
    
def top_correlated_features(df):
    corr_matrix = df.corr().abs()
    sol = (corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
                      .stack()
                      .sort_values(ascending=False))
    return sol.head(5)  

def split_and_merge(df, groupby_col = 'last_connection'):
    df.dropna(inplace = True)
    
    df_t = df.groupby(['last_connection'])[['t1', 't2']].mean().reset_index()
    df_t['last_connection'] = df_t.last_connection.apply(minus_month)
    df_t.dropna(inplace  = True)

    df_x = df.groupby(['month','last_connection'])[['x1','x2','x3']].mean().reset_index()
    result = pd.merge(df_t, df_x, on = 'last_connection').groupby(groupby_col).mean()
    
    return result