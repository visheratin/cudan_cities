# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 11:06:08 2020

@author: Ksenia Mukhina
"""
import streamlit as st
import pandas as pd
import pydeck as pdk
import app_utils

folder = 'data/'   
cities = {'London, UK': 'london', 
      'Saint Petersburg, Russia': 'spb',
      'Vienna, Austria': 'wienna', 
      'New York City, USA': 'new-york', } #'tokyo'

coordinates = {'london':(51.507222, -0.1275), 
          'spb':(59.9375, 30.308611),
          'wienna':(48.2, 16.366667), 
          'new-york':(40.71274, -74.005974),
          'kyoto':(35.0078, 135.7502),
          'tokyo':(),
          }

          
@st.cache
def load_data(city):
    map_data = pd.read_csv(folder + city + '-filtered.csv')
    map_data.columns =[x.lower() for x in map_data.columns]
    
    return map_data


def main():
    main_area = st.empty()    
    main_window(main_area)
    
    st.sidebar.title('Hi')
    page = st.sidebar.selectbox("See pages",
        ["Genral information", "City"])
    
    if page == "City":
        main_area.empty()
        complex_data()
    
def main_window(area):
    stats = []
    for city, fname in cities.items():
        map_data = pd.read_csv(folder + fname + '-filtered.csv')
        c = {}
        c['City'] = city
        c['Instagram locations'] = len(map_data)
        c['Posts since 2017'] = sum(map_data.iloc[:, 6:].sum(axis=1))
        stats.append(c)
        
    df = pd.DataFrame(stats)
    
    with area.beta_container():
        st.title('City analysis')
        
        st.subheader('City coverage by Instagram locations')
        
        #st.write("Here's our first attempt at using data to create a table:")
        st.write(df)
        
        option = st.selectbox(
            'Select city',
             list(cities.keys()))
        
        st.map(load_data(cities[option]))

def filter_data(map_data, date, value = 0):
    tmp = map_data[map_data[date] > value]
    return tmp[['lon','lat', date]]
    
def complex_data():     
     option = st.selectbox(
            'Select city',
             list(cities.keys()), key=1)
     
     map_data = load_data(cities[option])
     
     sl_date = st.select_slider('', app_utils.date_range())

     date = str(sl_date.year) + '-' + str(sl_date.month)
     
     st.pydeck_chart(pdk.Deck(
         map_style='mapbox://styles/mapbox/dark-v9',
         initial_view_state=pdk.ViewState(
             latitude=coordinates[cities[option]][0],
             longitude=coordinates[cities[option]][1],
             zoom=10,
             pitch=0,
         ),
         layers=[
             pdk.Layer(
                'HexagonLayer',
                data= filter_data(map_data, date, 5),
               get_position='[lon, lat]',
                radius=200,
                elevation_scale=0,
                pickable=True,
                extruded=False,
                color_aggregation="SUM",
                get_color_weight=date,
                color_range=app_utils.create_colors_from_hex(['#ffffb2','#fed976','#feb24c','#fd8d3c','#f03b20','#bd0026'])
                #[[241,238,246],[212,185,218],[201,148,199],
                 #            [223,101,176],[221,28,119],[152,0,67]]

             ),
    
         ],
     ))
     
     st.bar_chart(map_data[['2017-1', '2017-2', '2017-3', '2017-4', '2017-5', '2017-6', '2017-7',
       '2017-8', '2017-9', '2017-10', '2017-11', '2017-12', '2018-1', '2018-2',
       '2018-3', '2018-4', '2018-5', '2018-6', '2018-7', '2018-8', '2018-9',
       '2018-10', '2018-11', '2018-12', '2019-1', '2019-2', '2019-3', '2019-4',
       '2019-5', '2019-6', '2019-7', '2019-8', '2019-9', '2019-10', '2019-11',
       '2019-12', '2020-1', '2020-2', '2020-3', '2020-4', '2020-5', '2020-6',
       '2020-7', '2020-8', '2020-9', '2020-10', '2020-11', '2020-12']].sum(axis = 1))

if __name__ == "__main__":
    main()