# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 01:02:30 2021

@author: leona
"""

import io
from base64 import b64encode

import dash_cytoscape as cyto
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
    data = pd.read_csv("../Detram/datatran" + str(ano) + '.csv', delimiter = ';',  low_memory=False)
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

df2 = df.groupby(by=['Estado','Ano', 'Mês']).agg('sum').reset_index()


cyto.load_extra_layouts()

app = dash.Dash(__name__)
server = app.server

Estados = df2.Estado.unique()

app.layout = html.Div([
    dcc.Dropdown(
        id="selectstate",
        options=[{"label": x, "value": x} for x in Estados],
        placeholder = "Selecione o Estado"
    ),
    dcc.Graph(id="bar-chart"),
])

                  
@app.callback(
    Output("bar-chart", "figure"), 
    [Input("selectstate", "value")])
def update_bar_chart(estado):
    fig = px.bar(df2[df2["Estado"] == estado], x="Ano", y="Acidente", title="Quantidade de Acidentes por Estado", color = 'Mês')
    return fig


if __name__ == "__main__":
   app.run_server(debug=False, use_reloader=False, port = '8888')

