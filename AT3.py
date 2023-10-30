import pandas as pd
import os
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from jupyter_dash import JupyterDash

columns = ['data_inversa', 'mortos', 'municipio', 'uf', 'pessoas' ]
df = pd.DataFrame([], columns = columns)
for i,ano in enumerate(np.arange(2007,2022)):
    data = pd.read_csv("./Detram/datatran" + str(ano) + '.csv', delimiter = ';',  low_memory=False)
    df1 = data[columns]
    df = pd.concat([df,df1])
    

df = pd.DataFrame(df)
df['data_inversa'] = pd.to_datetime(df['data_inversa'])
df['pessoas'] = pd.to_numeric(df['pessoas'])
df['mortos'] = pd.to_numeric(df['mortos'])

df['acidentes'] = 1

n = df[df['uf'] =='(null)' ].index
df = df.drop(n)
df = df.rename({'data_inversa': 'Data', 'municipio': 'Municipio', 'pessoas': 'Pessoas', 'mortos': 'Mortos', 'acidentes': 'Acidente', 'uf': 'Estado'}, axis='columns')
df['Ano'] = df['Data'].dt.year 

df['Mês'] = df['Data'].dt.strftime('%B')

df = df.sort_values(by=['Estado', 'Municipio', 'Ano', 'Mês']) 
df1 = df.groupby(by=['Estado','Municipio','Ano','Mês']).agg('sum').reset_index()
#df.to_excel(r'./dataset.xlsx')
#data = pd.read_csv('./dataset.csv')