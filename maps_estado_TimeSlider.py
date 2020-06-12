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

brasilIO = pd.read_csv("./data/Brasil.io/BrasilIO.csv")
brasilIO = pd.read_csv("./data/BrasilIO_fixed.csv")
coordenadas = pd.read_csv("./data/coordinates.csv")
statesRawData = brasilIO.query('place_type == "state"')
statesGeoJson = folium.GeoJson("./data/brasil_estados.geojson")

states = gpd.read_file("./data/brasil_estados.geojson")
print(states.head())
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
print(dt_index)
# print(datetime_index)

styledata = {}

print(gdf.index)
print(states.index)
for country in gdf.index:
    # print(country)
    df = pd.DataFrame(
        {'color': np.random.normal(size=n_periods),
         'opacity': np.random.normal(size=n_periods)},
        index=dt_index
    )
    # df = df.cumsum()
    df.sample(n_sample, replace=False).sort_index()
    styledata[country] = df

# max_confirmed = statesRawData.max()[4]
# min_confirmed = statesRawData.min()[4]
# colorlist = [
#             '#FFAA00',
#             'red']
# indexlist = [
#             max_confirmed*0.1,
#             max_confirmed*0.75]
# colormap = cm.LinearColormap(colors=colorlist, index=indexlist,vmin=min_confirmed,vmax=max_confirmed)
# colormap.to_step(20)
min_val = 0
max_val = 100000
#CRIA UM COLOR RANGE LINEAR COM 10 ETAPAS
#colormap = cm.LinearColormap(colors=colorlist, index=indexlist,vmin=min_val,vmax=max_val)
colormap = cm.LinearColormap(colors=['#FFAA00','red'], index=[min_val,max_val],vmin=min_val,vmax=max_val)

# colormap
colormap.to_step(7,method='log')

estados = states["uf_05"]
styledict = {}
count_estados = 0
for i in estados:
    est_df = statesRawData.query('state=="'+i+'"')
    count = 0
    estadodict = {}
    for j in dias:
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
                                        'weight': 10,
                                        'dashArray': '5'}
        count = count + 1
    styledict[count_estados] = estadodict
    count_estados = count_estados + 1

res = dict(list(styledict.items())[0: 1])
# print(res) 

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

m.save(os.path.join('results', 'mapa_estado_timeSlider.html'))
