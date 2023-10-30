# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 11:57:03 2021

@author: leona
"""

import pandas as pd
import numpy as np
import plotly.express as px

columns = ['data_inversa', 'uf', 'mortos']
AC = []
data = pd.DataFrame(columns=columns)

for i,ano in enumerate(np.arange(2007,2022)):
   
    
   AC.append(pd.read_csv("./Detram/datatran" + str(ano) + '.csv', sep = ';'))
    
   df = AC[i].loc[:, columns]
   
   data = pd.concat([data,df], ignore_index=True)

data['ano'] = pd.DatetimeIndex(data['data_inversa']).year


dataMortes = data.groupby(['ano', 'uf'])['mortos'].sum().reset_index(name='mortos')
dataAcidentes = data.groupby(['ano', 'uf']).size().reset_index(name='acidentes')

dataMortes['acidentes'] = dataAcidentes.acidentes
fig = px.bar(dataAcidentes, x = 'ano', y = 'acidentes', color='uf', title="Quantidade de Acidente por Estado")
fig.show()

fig = px.scatter(dataMortes, x="acidentes", y="mortos", animation_frame="ano", animation_group="uf",
           size="mortos", color="uf", hover_name="uf",
           log_x=True)

fig["layout"].pop("updatemenus") # optional, drop animation buttons
fig.show()
    
    