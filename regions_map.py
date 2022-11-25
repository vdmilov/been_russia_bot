import json
import plotly.express as px
import db
import plotly.io as pio
import kaleido

with open('regions.json', 'r') as openfile:
    regions_geo = json.load(openfile)


def map_to_send(user_id):
    fig = px.choropleth_mapbox(data_frame=db.finish(user_id),
                               geojson=regions_geo,
                               featureidkey='properties.cartodb_id',
                               locations='region_id',
                               center={"lat": 69, "lon": 105},
                               zoom=1.7,
                               mapbox_style="open-street-map",
                               width=900,
                               height=500)

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, showlegend=False)
    fig_bytes = fig.to_image(format='png')
    return fig_bytes
