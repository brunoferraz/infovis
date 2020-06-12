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


assert 'naturalearth_lowres' in gpd.datasets.available

gdf = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# brasilIO = pd.read_csv("./data/Brasil.io/BrasilIO.csv")
brasilIO = pd.read_csv("./data/BrasilIO_municipios_fixed.csv")
# coordenadas = pd.read_csv("./data/coordinates.csv")
statesRawData = brasilIO.query('place_type == "city"')
# statesGeoJson = folium.GeoJson("./data/brasil_estados.geojson")

states = gpd.read_file("./data/BR_Localidades_2010_v1.geojson")
states = gpd.read_file("./data/municipio.json")
# print(states.head())
# print(statesGeoJson)

ax = gdf.plot(figsize=(10, 10))

start_date  = date(2020,2,25)
# end_date    = date.today()
end_date    = date(2020,6,9)
delta = int((end_date - start_date).days)
dias = []
for i in range(delta):
    day = start_date + timedelta(i)
    dias.append("20"+day.strftime("%y-%m-%d"))

n_periods, n_sample = delta, delta


datetime_index = pd.date_range('20'+start_date.strftime("%y-%m-%d"), periods=n_periods,)
dt_index_epochs = datetime_index.astype(int) // 10**9
dt_index = dt_index_epochs.astype('U10')


max_confirmed = statesRawData.max()[4]
min_confirmed = statesRawData.min()[4]
colorlist = [
            '#FFAA00',
            'red']
indexlist = [
            max_confirmed*0.1,
            max_confirmed*0.75]
colormap = cm.LinearColormap(colors=colorlist, index=indexlist,vmin=min_confirmed,vmax=max_confirmed)
colormap.to_step(20)

# for i in states:
#     print(i)

#REMOVE REPEATED CODES
list_codigo = states["CD_GEOCODMU"].values
list_codigo_cleaned = []
for i in list_codigo:
    if i  not in list_codigo_cleaned:
        list_codigo_cleaned.append(i)
list_codigo_cleaned.sort()
estados = list_codigo_cleaned


styledict = {}
count_estados = 0
total = len(estados[:20])
for i in estados[:20]:
    print(count_estados, "/", total)
    est_df = statesRawData.query('city_ibge_code=="'+i+'"')
    if(not est_df.empty):
        count = 0
        estadodict = {}
        for j in dias[:10]:
            df = est_df.query('date == "'+j+'"')
            qtd = df["confirmed"].values[0]
            cor =  colormap(qtd)
            alpha = 0.0
            if qtd<100:
                alpha = qtd/100.0
            else:
                alpha = 1
            estadodict[dt_index[count]] = {'color': cor,
                                            'opacity': alpha,
                                            }
            count = count + 1
        styledict[count_estados] = estadodict
        count_estados = count_estados + 1

res = dict(list(styledict.items())[0: 1])
print(res) 

from folium.plugins import TimeSliderChoropleth

m = folium.Map(
    # width = 600, height = 400,
    location=[-15.77972, -47.92972],
    # line_opacity = 0,
    zoom_start=5,
    tiles='OpenStreetMap')
# m.save(os.path.join('results', 'TimeSliderChoropleth_before_v2.html'))

g = TimeSliderChoropleth(
    # columns=["state","confirmed"],
    # key_on='feature.properties.uf_05',
    data = states.to_json(),
    styledict=styledict,
).add_to(m)
# colormap = cm.linear.Set1.scale(0, 35).to_step(10)
colormap.caption = 'Casos confirmados'
m.add_child(colormap)

m.save(os.path.join('results', 'TimeSliderChoropleth_municipio_working_v2.html'))
