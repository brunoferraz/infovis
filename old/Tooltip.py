#Contaminações Estático

# obter state, confirmed
casos_estados = base_brasil_io.loc[base_brasil_io.is_last == True, ['state', 'place_type', 'confirmed']]
casos_estados = casos_estados.loc[casos_estados.place_type == 'state']
casos_estados.drop(columns='place_type', inplace=True)
casos_estados.head()

coordCapitais = {
    'AC': [ -8.77, -70.55]
  , 'AL': [ -9.71, -35.73]
  , 'AM': [ -3.07, -61.66]
  , 'AP': [  1.41, -51.77]
  , 'BA': [-12.96, -38.51]
  , 'CE': [ -3.71, -38.54]
  , 'DF': [-15.83, -47.86]
  , 'ES': [-19.19, -40.34]
  , 'GO': [-16.64, -49.31]
  , 'MA': [ -2.55, -44.30]
  , 'MT': [-12.64, -55.42]
  , 'MS': [-20.51, -54.54]
  , 'MG': [-18.10, -44.38]
  , 'PA': [ -5.53, -52.29]
  , 'PB': [ -7.06, -35.55]
  , 'PR': [-24.89, -51.55]
  , 'PE': [ -8.28, -35.07]
  , 'PI': [ -8.28, -43.68]
  , 'RJ': [-22.84, -43.15]
  , 'RN': [ -5.22, -36.52]
  , 'RO': [-11.22, -62.80]
  , 'RS': [-30.01, -51.22]
  , 'RR': [  1.89, -61.22]
  , 'SC': [-27.33, -49.44]
  , 'SE': [-10.90, -37.07]
  , 'SP': [-23.55, -46.64]
  , 'TO': [-10.25, -48.25]
}

# necessário para delimitação dos estados
r = rq.get('https://raw.githubusercontent.com/TamyresBezerra/dadostrabalho/master/br_states.json')

filename = "br_states.json"
myfile = open(filename, 'w')
myfile.write(r.text)
myfile.close()

br_estados = 'br_states.json'
geo_json_data = json.load(open(br_estados, 'r'))

# contaminação por estado - atualmente
mapa = folium.Map(
    location=[-15.77972, -47.92972], 
    zoom_start=4,
    min_zoom=3, 
    max_zoom=5
)

folium.GeoJson(
    geo_json_data,
    name='Contaminação por estado',
    style_function=lambda feature: {
        'color': 'black',
        'weight': 0.3,
    }
    
).add_to(mapa)

for i in range(len(casos_estados)):
    folium.Circle(
        location=[coordCapitais[casos_estados.iloc[i]['state']][0], coordCapitais[casos_estados.iloc[i]['state']][1]],
        color='crimson', fill='crimson',
        tooltip='<li><bold>Estado: '+ str(casos_estados.iloc[i]['state']) + 
                '<li><bold>Confirmados: ' + str(casos_estados.iloc[i]['confirmed']),
        radius=int(casos_estados.iloc[i]['confirmed'])*7
    ).add_to(mapa)

# colormap.caption = 'Taxa de contaminação por estado'
# colormap.add_to(mapa)
folium.LayerControl(collapsed=False).add_to(mapa)

mapa.save('contaminação_estado.html')

mapa