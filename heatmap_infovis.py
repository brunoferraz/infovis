import pandas as pd
import plotly.graph_objects as go
import pandas as pd
import folium
import json
from datetime import timedelta, date

brasilIO = pd.read_csv("./data/Brasil.io/BrasilIO.csv")
brasilIO = pd.read_csv("./data/data_brasil_covid_fixed.csv")
coordenadas = pd.read_csv("./data/coordinates.csv")
statesRawData = brasilIO.query('place_type == "state"')
statesGeoJson = folium.GeoJson("./data/brasil_estados.geojson")

states_geo = "./data/brasil_estados.geojson"

with open(states_geo) as states_files:
    states_json = json.load(states_files)

# pega todos os estados no arquivo geojson
estados_lista = []
for index in range(len(states_json['features'])):
    estados_lista.append(states_json['features'][index]['properties']['uf_05'])


df = statesRawData
# pela lista de estados localiza os estados que nao informaram algum dia
for i in estados_lista:
    print(i)

start_date  = date(2020,2,25)
end_date    = date.today()
print(start_date)
print(end_date)
print(end_date - start_date)


# df.info()

df = statesRawData.query('date == "2020-05-24"')
# print(df)


m = folium.Map(
    width = 600, height = 400,
    location=[-15.77972, -47.92972],
    zoom_start=3
)
# m.choropleth(
#     geo_data = states_geo,
#     data = df,
#     columns=["state","confirmed"],
#     key_on='feature.properties.name',
#     fill_color='YlGnBu', 
#     fill_opacity=1, 
#     line_opacity=1,
#     legend_name='Births per 1000 inhabitants',
#     smooth_factor=0
# )
bins = list(statesRawData['confirmed'].quantile([0.0, 0.25, 0.5, 0.75, 1.0], interpolation='linear'))
# bin = [0, 4100]
print(bins)
folium.Choropleth(
    geo_data = states_geo,
    name='choropleth',
    data=df,
    columns=["state","confirmed"],
    key_on='feature.properties.uf_05',
    fill_color='OrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    bins = bins,
).add_to(m)
# folium.LayerControl().add_to(m)
m.save('index.html')