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


# assert 'naturalearth_lowres' in gpd.datasets.available

brasilIO = pd.read_csv("./data/BrasilIO_municipios_fixed.csv")
statesRawData = brasilIO.query('place_type == "city"')
dadosPath = "./data/municipio_new.json"
statesGeoJson = folium.GeoJson(dadosPath)
states = gpd.read_file(dadosPath, enconding='utf8')

# testeData = statesRawData.query('date == "2020-05-01"')
# m = folium.Map(
#     # width = 600, height = 400,
#     location=[-15.77972, -47.92972],
#     # line_opacity = 0,
#     zoom_start=5,
#     tiles='OpenStreetMap')
# folium.Choropleth(
#     geo_data = dadosPath,
#     name='choropleth',
#     data=testeData,
#     columns=["city_ibge_code","confirmed"],
#     key_on='feature.properties.GEOCODIGO',
#     # style_function = colormap,
#     fill_color='OrRd',
#     # fill_color=colormap.,
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     # bins = bins3,
# ).add_to(m)
# m.save(os.path.join('results', 'teste_new.html'))

#RANGE DE DIAS
start_date  = date(2020,2,25)
# end_date    = date.today()
end_date    = date(2020,6,9)
delta = int((end_date - start_date).days)
dias = []
for i in range(delta):
    day = start_date + timedelta(i)
    dias.append("20"+day.strftime("%y-%m-%d"))

# #FORMATA OS DIAS PARA O TimeSliderChoropleth
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
colormap.to_step(5)

# states = statesRawData.query('city_ibge_code == "3550308"')
print(states)

# # #REMOVE REPEATED CODES
# list_codigo = states["GEOCODIGO"].values
# list_codigo_cleaned = []
# for i in list_codigo:
#     if i  not in list_codigo_cleaned:
#         list_codigo_cleaned.append(i)
#         if(len(list_codigo_cleaned)==1000):
#             break
# list_codigo_cleaned.sort()
# estados = list_codigo_cleaned

estados = states["GEOCODIGO"].values
styledict = {}
count_estados = 0
total = len(estados)
for i in estados:
    print(count_estados, "/", total)
    est_df = statesRawData.query('city_ibge_code=="'+str(i)+'"')

    if(est_df.empty):
        count = 0
        estadodict = {}
        for j in dias:
            # cor = ';#ffaa00ff'
            # alpha = 1
            cor = "#FF00FF"
            estadodict[dt_index[count]] = {'color': cor,
                                            'opacity': alpha,
                                            }
            count = count + 1
    else:
        count = 0
        estadodict = {}
        est_df.set_index("date", inplace = True)
        for j in dias:
            df = est_df.loc[j]
            qtd = df["confirmed"]
            cor = colormap(qtd)
            # cor = "#ffaa00ff"
            alpha = 1
            estadodict[dt_index[count]] = {'color': cor,
                                            'opacity': alpha,
                                            }
            count = count + 1
    styledict[count_estados] = estadodict
    count_estados = count_estados + 1

res = dict(list(styledict.items())[0: 1])
# print(res)
# print(styledict)
# print(len(styledict))



from folium.plugins import TimeSliderChoropleth

m = folium.Map(
    # width = 600, height = 400,
    location=[-15.77972, -47.92972],
    # line_opacity = 0,
    zoom_start=5,
    tiles='OpenStreetMap')
# # m.save(os.path.join('results', 'TimeSliderChoropleth_before_v2.html'))

g = TimeSliderChoropleth(
    data = dadosPath,
    styledict=styledict,
).add_to(m)
colormap.caption = 'Casos confirmados'
m.add_child(colormap)

m.save(os.path.join('results', 'mapa_municipio_TimeSlider.html'))

# testeData = statesRawData.query('date == "2020-05-01"')
# m = folium.Map(
#     # width = 600, height = 400,
#     location=[-15.77972, -47.92972],
#     # line_opacity = 0,
#     zoom_start=5,
#     tiles='OpenStreetMap')
# folium.Choropleth(
#     geo_data = dadosPath,
#     name='choropleth',
#     data=testeData,
#     columns=["city_ibge_code","confirmed"],
#     key_on='feature.properties.GEOCODIGO',
#     style_function = styledict,
#     fill_color='OrRd',
#     # fill_color=colormap.,
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     # bins = bins3,
# ).add_to(m)
# m.save(os.path.join('results', 'teste_new.html'))