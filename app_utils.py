# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 11:00:44 2020

@author: Ksenia Mukhina
"""
import datetime
from dateutil.relativedelta import relativedelta

def create_colors_from_hex(colors):
    output_colors = [hex_to_rgb(c) for c in colors]
    return output_colors
        

def hex_to_rgb(color_string):
    h = color_string.lstrip('#')
    rgb_color = [int(h[i:i+2], 16) for i in (0, 2, 4)]
    return rgb_color

def date_range():
    start = datetime.datetime(2017, 1, 1)
    end = datetime.datetime(2020, 12, 1)
    
    rang = [start]
    while start < end:
        start += relativedelta(months=1)
        rang.append(start)
        
    return rang