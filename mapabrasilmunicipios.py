import os
import pandas as pd
import plotly.graph_objects as go
import pandas as pd
import folium
import json
from datetime import timedelta, date
import branca
import branca.colormap as cm
import geopandas as gpd
import numpy as np
# from google.colab import drive
import math

# drive.mount("drive")

# #dados covid
# brasilIO = pd.read_csv("drive/My Drive/Colab Notebooks/data/BrasilIO_municipios_fixed.csv")
# statesRawData = brasilIO.query('place_type == "city"')
# #GeoDados brasil
# # statesGeoJson = folium.GeoJson("drive/My Drive/Colab Notebooks/data/brasil_estados.geojson")
# geodados_path = "drive/My Drive/Colab Notebooks/data/municipio_new.json"
# geoDataCitys = gpd.read_file(geodados_path, enconding='utf8')

brasilIO = pd.read_csv("./data/BrasilIO_municipios_fixed.csv")
statesRawData = brasilIO.query('place_type == "city"')
geodados_path = "./data/municipio_new.json"
# geoDataCitys = folium.GeoJson(geodados_path)
geoDataCitys = gpd.read_file(geodados_path, enconding='utf8')

"""DEFINE O RANGE DE DIAS A PROCESSAR"""

#RANGE DE DIAS
start_date  = date(2020,2,25)
# end_date    = date.today()
end_date    = date(2020,6,9)
delta = int((end_date - start_date).days)
dias = []
for i in range(delta):
    day = start_date + timedelta(i)
    dias.append("20"+day.strftime("%y-%m-%d"))

"""FORMATA OS DIAS PARA O TimeSliderChoropleth

A quick solution I found is to convert the DatetimeIndex object to integer values (unix time in nanoseconds) and then to strings:
"""

# #FORMATA OS DIAS PARA O TimeSliderChoropleth
n_periods, n_sample = delta, delta
datetime_index = pd.date_range('20'+start_date.strftime("%y-%m-%d"), periods=n_periods,)
dt_index_epochs = datetime_index.astype(int) // 10**9
dt_index = dt_index_epochs.astype('U10')
dt_index

"""DEFINE COLOR RANGE"""

min_val = 0
max_val = 100000
#CRIA UM COLOR RANGE LINEAR COM 10 ETAPAS
#colormap = cm.LinearColormap(colors=colorlist, index=indexlist,vmin=min_val,vmax=max_val)
colormap = cm.LinearColormap(colors=['#FFAA00','red'], index=[min_val,max_val],vmin=min_val,vmax=max_val)

# colormap
colormap.to_step(7,method='log')

# geoDataCitys

# # #REMOVE REPEATED CODES
# list_codigo = geoDataCitys["GEOCODIGO"].values
# list_codigo_cleaned = []
# for i in list_codigo:
#     if i  not in list_codigo_cleaned:
#         list_codigo_cleaned.append(i)
# list_codigo_cleaned.sort()
# estados = list_codigo_cleaned
# len(estados)

cities = geoDataCitys["GEOCODIGO"].values
styledict = {}
count_cities = 0
total = len(cities)
for i in cities:
    print(count_cities, "/", total)
    est_df = statesRawData.query('city_ibge_code=="'+str(i)+'"')
    # se o dataframe estiver vazio
    if(est_df.empty):
      count = 0
      city_dict = {}
      # percorre os dias
      for j in dias:
        #cria estilo vazio
        cor = '#ff00ff'
        alpha = 1
        city_dict[dt_index[count]] = {'color':cor, 'opacity':alpha}
        count = count + 1
    # se o dataframe estiver cheio
    else:
      count = 0
      city_dict = {}
      est_df.set_index("date", inplace = True)
      #percorre os dias
      for j in dias:
        #cria estilo com info
        df = est_df.loc[j]
        qtd = df['confirmed']
        cor = colormap(qtd)
        alpha = 1
        city_dict[dt_index[count]] = {'color':cor, 'opacity':alpha}
        count = count + 1
    styledict[count_cities] = city_dict
    count_cities = count_cities + 1


from folium.plugins import TimeSliderChoropleth
m = folium.Map(
    location=[-15.77972, -47.92972],
    # line_opacity = 0,
    zoom_start=5,
    tiles='OpenStreetMap')

g = TimeSliderChoropleth(
    data = geodados_path,
    styledict = styledict,
).add_to(m)
# colormap = cm.linear.Set1.scale(0, 35).to_step(10)
colormap.caption = 'Casos confirmados'
m.add_child(colormap)
m.save(os.path.join('results', 'mapa_municipio_timeSlider.html'))