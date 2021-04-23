#%%
import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

df = gpd.read_file( r"C:\Users\csucuogl\Desktop\WORK\MISC_TEST\Replica_Transit\Elif_Data2.shp" )
df = df.to_crs(epsg=4326)
df['R_total_ch'] = df['R_total_ch'].astype(float)
df.head()

# %%
import json 


poly_json = json.loads(df['geometry'].to_json())

fig = go.Figure()


path = r"C:\Users\csucuogl\Desktop\DATA\NYC\Bicycle Routes\Routes_1.shp"
dfp = gpd.read_file( path )
dfp = dfp.to_crs(epsg=4326)
#dfp = dfp.sample( 250 )


fig.add_trace(
    go.Choroplethmapbox(
        geojson=poly_json, # Spatial coordinates
        locations = df.index,
        z = df['R_total_ch'],
        marker_opacity = 0.25
    )
)



for i,r in dfp['geometry'].iteritems():

    try:
        lats =  list( r.xy[0] ) 
        lons =  list( r.xy[1] ) 

        fig.add_trace(
            go.Scattermapbox(
                mode = "lines",
                lon = lats,
                lat = lons,
                hoverinfo='none',
                line = dict(width = 1,color = 'black')
            )
    )
    except:

        for l in r:
            lats = list( l.xy[0] ) 
            lons = list( l.xy[1] ) 

            fig.add_trace(
                go.Scattermapbox(
                    mode = "lines",
                    lon = lats,
                    lat = lons,
                    hoverinfo='none',
                    line = dict(width = 1,color = 'black')
                )
        )


fig.update_layout(mapbox_style="carto-positron",mapbox_zoom=9,mapbox_center={"lat": 40.71, "lon": -74.00})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0} , showlegend=False)
fig.show()

# %%
lats

# %%
