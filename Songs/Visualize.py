#%% IMPORT DEPENDENCIES
import pandas as pd
import networkx as nx
import os
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.graph_objects as go

# %% IMPORT ALL DATA IN FROM LOCAL FOLDER

mypath = r'C:\Users\csucuogl\Documents\GitHub\IdeasTesting\Songs\data'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

df = pd.DataFrame()
for _ in onlyfiles:
    temp = pd.read_csv( os.path.join(mypath,_) )
    df = df.append( temp )

df = df[df['pts_from']!='points received']
df.sample(5)

# %% FORMAT

df['pts_from'] = df['pts_from'].str.upper()
df['points_to'] = df['points_to'].str.upper()

df['pts_from'] = df['pts_from'].replace('-',' ' , regex = True )
df['points_to'] = df['points_to'].replace('-',' ' , regex = True )

total_score = df.groupby('year').sum()['pts']

#n_points contains normalized scores. score/total score of that year
dfn = pd.DataFrame()
for y in df['year'].unique():
    total = total_score[total_score.index == y ].tolist()[0] 
    temp = df[ df['year']== y ].copy()
    temp['n_pts'] = temp['pts'] / total
    dfn = dfn.append( temp )

dfn

#%% FORMATTING
dfn = dfn[ ~dfn['points_to'].isin(['MONACO','MOROCCO']) ]
dfn = dfn[ ~dfn['pts_from'].isin(['MONACO','MOROCCO']) ]

dfn['region'] = None

dfn.loc[ dfn['pts_from'].isin(['SWEDEN','DENMARK','NORWAY','FINLAND','ICELAND']) , 'region' ] = 'Scandinavia'
dfn.loc[ dfn['pts_from'].isin(['PORTUGAL','SPAIN','ITALY','GREECE']) , 'region' ] = 'Southern Europe'
dfn.loc[ dfn['pts_from'].isin(['YUGOSLAVIA','RUSSIA','BOSNIA & HERZEGOVINA','SLOVENIA','CROATIA','POLAND','HUNGARY','ROMANIA','SLOVAKIA','NORTH MACEDONIA','ESTONIA','LITHUANIA']) , 'region' ] = 'Eastern Europe'
dfn.loc[ dfn['pts_from'].isin(['TURKEY','ISRAEL','CYPRUS','MALTA']) , 'region' ] = 'EMed'
dfn.loc[ dfn['pts_from'].isin(['FRANCE','BELGIUM','LUXEMBOURG','SWITZERLAND','GERMANY','AUSTRIA','THE NETHERLANDS']) , 'region' ] = 'Western Europe'
dfn.loc[ dfn['pts_from'].isin(['UNITED KINGDOM','IRELAND']) , 'region' ] = 'UK'

dfn

#%% Single Country Over Time
#Dropdown Layout

df2 = dfn[ dfn['year'] > 1970 ]

fig = go.Figure()
conts = df2['points_to'].unique().tolist()

down_list = []
for i in range(len(conts)):
    cont = conts[i]
    viz = [True if i==n else False for n in range(len(conts)) ]
    temp = df2[df2['points_to']== cont ]

    fig.add_trace( #Scatter
        go.Scatter( 
            x= [temp['region'],temp['pts_from']], 
            y= temp['year'],
            mode='markers',
            text = temp['pts'],
            hovertemplate = 'Points: %{text:.0f}<extra></extra>',
            marker=dict(
                color = '#f4a261',
                opacity = 0.4,
                size= temp['pts']*1.5,
                line=dict(width=0)
            ),
            showlegend = False,
        ))

    down_list.append( #creates template to be used in button arguments
        dict(
            args = [dict( visible = viz)] ,
            label = cont.capitalize(),
            method="update"
        ))

fig.update_layout( # General Layout
    margin=dict(l=15, r=5, t=40, b=15),
    paper_bgcolor="#f6f6f6",
    plot_bgcolor="#f2f2f2",
    font_family="Avalon",
    font_color="#5a5a5a",
    hoverlabel=dict( #Hover Styling
        bgcolor="#f6f6f6",
        font_size=9,
        font_family="Avalon",
        font_color="#5a5a5a"
    )
    )

fig.update_layout( # Add dropdown
    updatemenus=[
        dict(
            active = 0,
            buttons = list(down_list) ,
            direction="down",
            pad={"r": 0, "t": 0},
            showactive=True,
            x=0.16,
            xanchor="left",
            y=1.25,
            yanchor="top"
        ),
    ],
    annotations=[
        dict(text="Select a Country:", showarrow=False,
        x=0, y=1.22, yref="paper", align="left")
        ]
    )

fig.update_yaxes(nticks=25,range=[1960, 2020])
fig.show()

# %% Analysis as a network
# Take a random year - Map the voting a weighted/ directional network graph

import random

year = random.randint( dfn.year.min() , dfn.year.max() )
df1 = dfn[ dfn['year'] == 1977 ]

G = nx.DiGraph()

c_list = []
for i,r in df1.iterrows(): # Received Points
    G.add_edge(  r['points_to'] ,r['pts_from'], weight = r['n_pts'] )
    c_list.append( r['region'] )

ini_pos = nx.spring_layout(G,iterations=500)

#Color Map
color_list = []
for i in ini_pos.keys():
    _ = df1[ df1['pts_from'] == i ]['region'].unique()
    if _ == 'Scandinavia':color_list.append( 'red' )
    elif _ == 'Southern Europe':color_list.append( 'blue' )
    elif _ == 'Eastern Europe':color_list.append( 'purple' )
    elif _ == 'EMed':color_list.append( 'black' )
    elif _ == 'Western Europe':color_list.append( 'grey' )
    elif _ == 'UK':color_list.append( 'blue' )
    else:color_list.append( 'magenta' )

plt.figure(figsize=(18,12))
nx.draw(G, 
    pos = ini_pos, 
    with_labels=True,
    width= df1['n_pts'].multiply(800).tolist() ,
    edge_color="skyblue", style="solid",
    font_size=14,
    arrows=True,
    alpha=0.5,
    arrowstyle='<-'
    )

nx.draw_networkx_nodes(G, pos=ini_pos, node_size=200, node_color=color_list)

plt.title( str(year) )
plt.show()


# %%

