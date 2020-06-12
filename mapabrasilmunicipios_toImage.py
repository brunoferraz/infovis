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
dadosPath = "./data/municipio.json"
statesGeoJson = folium.GeoJson(dadosPath)

min_val = 0
max_val = 100000
# colorscale = branca.colormap.linear.YlGnBu_09.scale(0, 30)
# colormap = cm.LinearColormap(colors=['#FFAA00','red'], index=[min_val,max_val],vmin=min_val,vmax=max_val)
# colormap = cm.StepColormap(colors=['#ffffff','#ffff00','#ffaa00','#ffa800','#ff9900','#ff0000'], index=[0,10, 100, 1000, 10000, 100000],vmin=0, vmax=100000)
colormap = cm.LinearColormap(colors=['#ffffff','#ffff00','#ffaa00','#ffa800','#ff9900','#ff0000'], index=[0,10, 100, 1000, 10000, 100000],vmin=0, vmax=100000)
# colormap = colormap.to_step(6)

for i in range(len(dias)):
    testeData = statesRawData.query('date == "'+dias[i]+'"')
    mydata = testeData.set_index('city_ibge_code')['confirmed']

    # print(testeData.loc())
    def style_function(feature):
        confirmed = mydata.get(int(feature['properties']['GEOCODIGO']), None)
        cor = '#ffffff'
        if(confirmed != None):
            cor = colormap.rgb_hex_str(confirmed)
        return {
            'fillOpacity': 1,
            'weight': 0,
            'fillColor': cor
        }

    m = folium.Map(
        # width = 600, height = 400,
        location=[-15.77972, -47.92972],
        # line_opacity = 0,
        zoom_start=4.5,
        tiles='cartodbpositron')


    statesGeoJson = folium.GeoJson(data = dadosPath,
                                    style_function=style_function)
    statesGeoJson.add_to(m)
    m.add_child(colormap)
    m.save(os.path.join('paginas', 'mapa_'+str(i)+'.html'))
