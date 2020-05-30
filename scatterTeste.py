import plotly.graph_objects as go

import pandas as pd

df = pd.read_csv('./data/coordinates.csv')
# print(df['LONGITUDE'])
# fig = go.Figure()
# fig.show()
print(df['LATITUDE'])

fig = go.Figure(data=go.Scattergeo(
        lon = df['LONGITUDE'],
        lat = df['LATITUDE'],
        mode = 'markers',
        # marker_color = df['ALTURA']
        ))
fig.update_layout(
    geo_scope = 'south america'
)
fig.show()