# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 19:07:16 2018

@author: Serhii
"""

import sys
import json
from darksky import forecast
from datetime import datetime as dt

class DarkSkyWeather:
    
    API_KEY = "f47016c08a6a30275d7b9edc165cc766"
    
    def __init__(self):
        pass
        
        
    def avg_hourly(self, hourlyData):
        s = 0
        l = len(hourlyData)
        for i in range(l):
            s += hourlyData[i].temperature
            
        return round(s / l, 1)


    def get_year_weather(self, lat0, lng0, lat1, lng1, steps=12):
        data = {
            'avg_temperature': 0,
            'avg_cloud_cover': 0,
            'avg_humidity': 0,
            'set': []
        }
        day=86400
        year = 365*day
        step = year // steps
        t = round(dt.now().timestamp()) - year
        lat = round((lat0+lat1)/2, 6)
        lng = round((lng0+lng1)/2, 6)
        for i in range(steps):
            time = round(t + i * step)
            point = forecast(DarkSkyWeather.API_KEY, lat, lng, time)
                
            item = {
                'timestamp': time,
                'temperature': self.avg_hourly(point.hourly.data),
                'humidity': point.daily.data[0].humidity,
                'cloud_cover': point.daily.data[0].cloudCover
            }
            
            data['avg_temperature'] += item['temperature'] / steps
            data['avg_humidity'] += item['humidity'] / steps
            data['avg_cloud_cover'] += item['cloud_cover'] / steps

            data['set'].append(item)
            
        data['avg_temperature'] = round(data['avg_temperature'], 2)
        data['avg_humidity'] = round(data['avg_humidity'], 2)
        data['avg_cloud_cover'] = round(data['avg_cloud_cover'], 2)
        return data


if __name__ == '__main__':
    ds_weather = DarkSkyWeather()
    bbox = map(float, sys.argv[1:])

    result = ds_weather.get_year_weather(*bbox)

    with open('climate.json', 'w') as outfile:
        json.dump(result, outfile)


