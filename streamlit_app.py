# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 11:06:08 2020

@author: Ksenia Mukhina
"""
import numpy as np
import streamlit as st
import pandas as pd
import pydeck as pdk

folder = 'data/'   
cities = {'London, UK': 'london', 
      'Saint Petersburg, Russia': 'spb',
      'Vienna, Austria': 'wienna', 
      'New York City, USA': 'new-york', } #'tokyo'


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
        c['Posts since 2016'] = sum(map_data.iloc[:, 6:].sum(axis=1))
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

def complex_data():
     df = pd.DataFrame(
         np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
         columns=['lat', 'lon'])
     

     st.pydeck_chart(pdk.Deck(
         map_style='mapbox://styles/mapbox/light-v9',
         initial_view_state=pdk.ViewState(
             latitude=37.76,
             longitude=-122.4,
             zoom=11,
             pitch=50,
         ),
         layers=[
             pdk.Layer(
                'HexagonLayer',
                data=df,
               get_position='[lon, lat]',
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
             ),
    
         ],
     ))
  #  
      #  st.slider('', min_value=0, max_value=10)
        
if __name__ == "__main__":
    main()