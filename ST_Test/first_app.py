

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random

st.set_page_config(layout="centered",page_title='App Test')

@st.cache
def load_data(nrows): #Create dummy data
    gdf = pd.DataFrame(
        np.random.randn(nrows, 2) / [50, 50] + [37.76, -122.4],
        columns=['lat', 'lon'])
    gdf['name'] = [random.randint(1,10) for i in range(len(gdf))]
    gdf['test'] = [random.randint(1,100) for i in range(len(gdf))]
    return gdf

gdf = load_data(1000)


st.title('Fake Data')
st.subheader('Even more fake data thing.')

st.write("Here's our first attempt at using data to create a table:")
st.table(gdf.head(5))

s1, s2,s3 = st.beta_columns( (2,0.1,1) )

values = s1.slider( #Create a filter slider
    label = 'Select a range of values',
    min_value = 0 ,
    max_value = 10 ,
    value = ( 0,10 ),
    step = 1
    )

tests = s3.slider( #Create a filter slider
    label = 'Select a range of test',
    min_value = 0 ,
    max_value = 100 ,
    value = ( 0,100 ),
    step = 10
    )

gdf2 =  gdf[ (gdf['name']>values[0]) & (gdf['name']<values[1]) & (gdf['test']>tests[0]) & (gdf['test']<tests[1])   ].copy()
gdf2['bins'] = pd.qcut( gdf2['test'] , q=5,labels=['1st','2nd','3rd','4th','5th'] )

#Figure 1
fig = px.scatter_mapbox(gdf2,
                        lat=gdf2.lat,
                        lon=gdf2.lon,
                        hover_name='name',
                        size = 'name',
                        zoom=12)
fig.update_layout(mapbox_style="open-street-map",width = 480)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":15})

gr = gdf2.groupby( by=['name','test'] ).size().reset_index()
gr.columns = ['name','test','count']

#Figure 2
fig_hist = px.scatter( gr ,x='name',y='test',
    size='count')

fig_hist.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    width=250
    )
fig_hist.update_xaxes(range=[0,10])
fig_hist.update_yaxes(range=[0,105])
fig_hist.update_xaxes(title_text=None)
fig_hist.update_yaxes(title_text=None)

c1, c2,c3 = st.beta_columns( (2,0.1,1) )

c1.plotly_chart(fig)
c3.plotly_chart(fig_hist)

st.subheader('Continuing the Story from here')
st.write("I grouped these things and now I am curious what these can be.")
