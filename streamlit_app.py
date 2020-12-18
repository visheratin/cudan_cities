# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 11:06:08 2020

@author: Ksenia Mukhina
"""
import streamlit as st
import pandas as pd
import pydeck as pdk
import datetime
from dateutil.relativedelta import relativedelta

folder = 'data/'   
cities = {'London, UK': 'london', 
      'Saint Petersburg, Russia': 'spb',
      'Vienna, Austria': 'wienna', 
      'New York City, USA': 'new-york', } #'tokyo'

coordinates = {'london':(51.507222, -0.1275), 
          'spb':(59.9375, 30.308611),
          'wienna':(48.2, 16.366667), 
          'new-york':(40.71274, -74.005974), }

def hex_to_rgb(color_string):
    h = color_string.lstrip('#')
    rgb_color = [int(h[i:i+2], 16) for i in (0, 2, 4)]
    return rgb_color

def date_range():
    start = datetime.datetime(2017, 1, 1)
    end = datetime.datetime(2020, 1, 1)
    
    rang = [start]
    while start < end:
        start += relativedelta(months=1)
        rang.append(start)
        
    return rang
          
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
     
     sl_date = st.select_slider('', date_range())

     date = str(sl_date.year) + '-' + str(sl_date.month)
     
     st.pydeck_chart(pdk.Deck(
         map_style='mapbox://styles/mapbox/light-v9',
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
                color_range=[[241,238,246],[212,185,218],[201,148,199],
                             [223,101,176],[221,28,119],[152,0,67]]

             ),
    
         ],
     ))
                    #    get_fill_color=[255,0,0],
                #"[255, (1 -" + date + "/" + str(map_data[date].max()) + ") * 255, 0]",
              #  get_line_color=[255, 255, 255],
             #   line_width_min_pixels=2,
if __name__ == "__main__":
    main()