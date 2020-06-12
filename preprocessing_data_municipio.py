import pandas as pd
import plotly.graph_objects as go
import pandas as pd
import folium
import json
from datetime import timedelta, date

brasilIO = pd.read_csv("./data/Brasil.io/BrasilIO.csv")
coordenadas = pd.read_csv("./data/coordinates.csv")
citiesRawData = brasilIO.query('place_type == "city"')
# statesGeoJson = folium.GeoJson("./data/brasil_estados.geojson")
# statesGeoJson = folium.GeoJson("./data/BR_Localidades_2010_v1.geojson")
statesGeoJson = folium.GeoJson("./data/geojs-100-mun.json")

states_geo = "./data/BR_Localidades_2010_v1.geojson"

with open(states_geo, encoding="utf8") as states_files:
    states_json = json.load(states_files)

# pega todos os estados no arquivo geojson
cidades_lista = []
for index in range(len(states_json['features'])):
    # print(index)
    cidades_lista.append(states_json['features'][index]['properties']['CD_GEOCODMU'])


df = citiesRawData
# pela lista de estados localiza os estados que nao informaram algum dia
# for i in cidades_lista:
#     print(i)
# print(df.info())

start_date  = date(2020,2,25)
end_date    = date.today()
delta = int((end_date - start_date).days)
dias = []
for i in range(delta):
    day = start_date + timedelta(i)
    dias.append("20"+day.strftime("%y-%m-%d"))



#     # print(i)
#     df = statesRawData.query('date == "'+i+'" & state=="SP"')
#     df_perday.append(df)

print(len(cidades_lista))

list_data_per_city = []
list_empty_city = []
# cidades_lista = ['3550308']
print("1/5 -PEGA CIDADES")
counter = 0
total = len(cidades_lista)
for i in cidades_lista:
    counter = counter + 1
    print(counter," /" ,total)
    df = citiesRawData.query('city_ibge_code=="'+str(float(i))+'"')
    if(not df.empty):
        list_data_per_city.append(df)
    else:
        list_empty_city.append(i)
complete_data_per_city = {}
print("2/5 -PEGA INFO DAS DATAS POR ESTADO")
counter = 0
total = len(list_data_per_city)
for i in list_data_per_city:
    counter = counter + 1
    print(counter," /" ,total)
    key = i['city_ibge_code'].values[0]
    df_perday = []
    for j in dias:
        df = i.query('date == "'+j+'"')
        df_perday.append(df)
    complete_data_per_city[key] = df_perday

# print(type(complete_data_per_city))
# print(complete_data_per_city[0]['confirmed'])

# # Percorre todos os dados por estado:
print('3/5 -CORRIGE DADOS POR MUNICIPIO')
counter = 0
total = len(complete_data_per_city)
for city in complete_data_per_city:
    counter = counter + 1
    print(counter," /" ,total)
    datadias = complete_data_per_city[city]
#     # se o primeiro dia for vazio percorre a lista para frente ate encontrar o primeiro dia nao vazio
#     # pega toda a estrutura do dataframe e zera o valor
    if(datadias[0].empty):
        indice_com_informacao = 0
        for i in range(len(datadias)):
            if(not datadias[i].empty):
                indice_com_informacao = i
                break
        datadias[0] = datadias[indice_com_informacao].copy()
        datadias[0]['confirmed'].values[0] = 0
        # Fazer depois de ajustar todas as falhas
        # datadias[0]['date'].values[0] = dias[0]
        # print(datadias[0]['date'].values[0])
    last = datadias[0]
    for k in range(1, len(datadias)):
        if(datadias[k].empty):
            datadias[k] = last.copy()
        last = datadias[k]
    # ajustar datas dos relatorios
    for k in range(len(datadias)):
        datadias[k]['date'].values[0] = dias[k]
    
    # faz merge para um unico data frame por estado
    d = pd.concat(datadias)
    complete_data_per_city[city] = d

print('4/5 -CONCATENA MUNICIPIOS')
# #faz merge do brasil inteiro
brasil = []
counter = 0
total = len(complete_data_per_city)
for i in complete_data_per_city:
    counter = counter + 1
    print(counter," /" ,total)
    brasil.append(complete_data_per_city[i])

data_brasil = pd.concat(brasil)

print('5/5 -SALVA ARQUIVO')
data_brasil.to_csv('./data/BrasilIO_municipios_fixed.csv')

# df_perday[0].info()
# print(df_perday)

# for i in df_perday[:1]:
    # print(i['0'])
    # print(i.empty)
# base = {'city':[NaN], 'city_ibge_code':[NaN],  'confirmed':  confirmed_per_100k_inhabitants        date  death_rate  deaths  estimated_population_2019  is_last  order_for_place place_type state}