import pandas as pd
import plotly.graph_objects as go
import pandas as pd
import folium
import json
from datetime import timedelta, date

brasilIO = pd.read_csv("./data/Brasil.io/BrasilIO.csv")
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
# for i in estados_lista:
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

list_data_per_state = []
for i in estados_lista:
    df = statesRawData.query('state=="'+i+'"')
    list_data_per_state.append(df)
complete_data_per_state = {}
for i in list_data_per_state:
    key = i['state'].values[0]
    df_perday = []
    for j in dias:
        df = i.query('date == "'+j+'"')
        df_perday.append(df)
    complete_data_per_state[key] = df_perday

# Percorre todos os dados por estado:
for state in complete_data_per_state:
    datadias = complete_data_per_state[state]
    # se o primeiro dia for vazio percorre a lista para frente ate encontrar o primeiro dia nao vazio
    # pega toda a estrutura do dataframe e zera o valor
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
    complete_data_per_state[state] = d

#faz merge do brasil inteiro
brasil = []
for i in complete_data_per_state:
    brasil.append(complete_data_per_state[i])

data_brasil = pd.concat(brasil)
data_brasil.to_csv('./data/BrasilIO_fixed.csv')

# df_perday[0].info()
# print(df_perday)

# for i in df_perday[:1]:
    # print(i['0'])
    # print(i.empty)
# base = {'city':[NaN], 'city_ibge_code':[NaN],  'confirmed':  confirmed_per_100k_inhabitants        date  death_rate  deaths  estimated_population_2019  is_last  order_for_place place_type state}