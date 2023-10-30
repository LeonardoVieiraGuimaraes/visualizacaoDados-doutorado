# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 11:57:03 2021

@author: leona
"""

import pandas as pd
import os
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


AC = [ ]

Municipio = [ ]
MunicipioFreq = [ ]

UF = [ ]
UFFreq = [ ]

UFMortes = [ ]
UFMortesFreq = [ ]

for i,ano in enumerate(np.arange(2007,2022)):
   
    AC.append(pd.read_csv("./Detram/datatran" + str(ano) + '.csv', delimiter = ';'))
    
    Municipio.append(AC[i].loc[:, ['data', 'municipio']])
    MunicipioFreq.append(Municipio[i].groupby('municipio').size())
    
    UF.append(AC[i].loc[:, [uf']])
    # UFFreq.append(UF[i].value_counts(sort = True))
    UFFreq.append(UF[i].groupby('uf').size())
    # UFFreq.append(pd.crosstab(index=UF[i]['uf'], columns = 'Quantidade de acidentes'))
    
    UFMortes.append((AC[i].loc[:, ['uf', 'mortos']]))
    # UFMortesFreq.append(pd.pivot_table(UFMortes[i], values = 'mortos', index=['uf'], aggfunc=np.sum))
    # UFMortesFreq.append(pd.crosstab(index=UFMortes[i]['uf'], columns = UFMortes[i]['mortes'], margins=True))    
    UFMortesFreq.append(UFMortes[i].groupby('uf')['mortos'].sum())
    

dataMunicipio = (pd.DataFrame(MunicipioFreq, index = np.arange(2007,2022)))
dataEstado =  (pd.DataFrame(UFFreq, index = np.arange(2007,2022)))
dataEstadoMortos =  (pd.DataFrame(UFMortesFreq, index = np.arange(2007,2022)))


dataEstado.pop('(null)')
dataEstadoMortos.pop('(null)')

dataEstado.index.name = 'Ano'
dataEstado.columns.name = 'Estado'
dataEstadoMortos.index.name = 'Ano'
dataEstadoMortos.columns.name = 'Estado'


fig = px.bar(dataEstadoMortos,  title="Quantidade de Acidente por Estado")
fig.show()

fig = px.scatter(dataEstadoMortos, x = 'Estado', y = 'Ano')
fig.show()


import plotly.express as px

df = px.data.gapminder()
fig = px.scatter(dataEstadoMortos, x="Estado", y="Ano", animation_frame="year", animation_group="country",
           size="pop", color="Estado", hover_name="country",
           log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])

fig["layout"].pop("updatemenus") # optional, drop animation buttons
fig.show()    
    
    