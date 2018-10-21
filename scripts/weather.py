import sys
import json
from datetime import datetime as dt
import requests
from random import randint
from utils import create_net


class DarkSkyWeather:

    NET_STEP = 0.01
    MAX_QTY = 36
    API_KEYS = [
        'f47016c08a6a30275d7b9edc165cc766',
        '52d613b3bd28a5132972ce3889fc11a2',
        '406abf7da441a9e367bd22b23c7d74c7',
        '0e8fd2784b8b018d6a9b13299a47a180',
        'f54572f11ec89677936a436cf24e2f80'
    ]
    BASE_URL = 'https://api.darksky.net'
    FORECAST_URL = '/forecast/{key}/{lat},{lng},{timestamp}'
    
    def __init__(self):
        pass

    @staticmethod
    def net_by_quantity(lat0, lng0, lat1, lng1, qty=36):
        steps = round(qty**(1/2)) + 1
        step_lat = (lat1 - lat0) / steps
        step_lng = (lng1 - lng0) / steps
        net = []
        for i in range(1, steps):
            for j in range(1, steps):
                net.append((lat0 + i * step_lat, lng0 + j * step_lng))
        return net

    def request(self, lat, lng, time):
        key = self.API_KEYS[randint(0, len(self.API_KEYS) - 1)]
        return requests.get(
            self.BASE_URL + self.FORECAST_URL.format(
                key=key,
                lat=str(lat),
                lng=str(lng),
                timestamp=str(time)
            )
        ).json()

    @staticmethod
    def avg_hourly(hourly_data):
        s = 0
        l = len(hourly_data)
        for i in range(l):
            s += hourly_data[i]['temperature']
        return round(s / l, 1)

    def get_year_weather(self, lat0, lng0, lat1, lng1, steps=12):
        data = []
        day = 86400
        year = 365*day
        step = year // steps
        t = round(dt.now().timestamp()) - year
        net = create_net(lat0, lng0, lat1, lng1, self.NET_STEP)
        if len(net) > self.MAX_QTY:
            net = self.net_by_quantity(lat0, lng0, lat1, lng1, self.MAX_QTY)
        print(len(net))
        for coordinates in net:
            data_item = {
                'temperature': 0,
                'cloud_cover': 0,
                'humidity': 0
            }
            lat = round(coordinates[0], 6)
            lng = round(coordinates[1], 6)
            print(lat, lng)
            for i in range(steps):
                time = round(t + i * step)
                point = self.request(lat, lng, time)
                data_item['temperature'] += self.avg_hourly(point['hourly']['data']) / steps
                data_item['humidity'] += point['daily']['data'][0]['humidity'] / steps
                data_item['cloud_cover'] += point['daily']['data'][0]['cloudCover'] / steps

            # convert Fahrenheit to Celsius
            data_item['temperature'] = round((data_item['temperature'] - 32) * 5 / 9, 2)
            data_item['humidity'] = round(data_item['humidity'], 2)
            data_item['cloud_cover'] = round(data_item['cloud_cover'], 2)
            data.append({
                "coordinates": [lat, lng],
                "response": data_item
            })
        return data


if __name__ == '__main__':
    ds_weather = DarkSkyWeather()
    bbox = map(float, sys.argv[1:])

    result = ds_weather.get_year_weather(*bbox)

    with open('climate.json', 'w') as outfile:
        json.dump(result, outfile)
