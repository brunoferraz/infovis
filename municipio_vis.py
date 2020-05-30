# import plotly.graph_objects as go
# fig = go.Figure(data=go.Bar(y=[2, 3, 1]))
# fig.write_html('first_figure.html', auto_open=True)

# import plotly.graph_objects as go

# fig = go.FigureWidget(data=go.Bar(y=[2, 3, 1]))
# fig.show()

from urllib.request import urlopen
import json
import urllib3
import urllib
print("passou")
# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
# with urlopen('file:///C:/Users/Bruno/Documents/dev/infovis/data/geojson-counties-fips.json') as response:
with urlopen('file:///C:/Users/Bruno/Documents/dev/infovis/data/municipal-brazilian-geodata/data/RJ.json') as response:
    
# with urllib3.request.urlopen('file://geojson-counties-fips.json') as respose:
    counties = json.load(response)

import pandas as pd
# df = pd.read_csv("./data/fips-unemp-16.csv",
#                    dtype={"fips": str})
df = pd.read_csv("./data/covid19rio.csv",
                   dtype={"GEOCODIGO": str})


# ndf = pd.read_csv("./")

import plotly.express as px

fig = px.choropleth_mapbox(df, 
                            geojson=counties, 
                            locations='GEOCODIGO', 
                            color='last_available_confirmed',
                           color_continuous_scale="Viridis",
                           range_color=(0, 10000),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": -15.7940873613963, "lon": -47.8879054780314},
                        #    opacity=0.5,
                        #    labels={'unemp':'unemployment rate'}
                          )
fig.update_layout(margin={"r":10,"t":10,"l":10,"b":10})
fig.show()
print("chegou aqui")