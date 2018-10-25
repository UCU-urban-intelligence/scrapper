from scripts.weather import DarkSkyWeather
from shapely.geometry import Point


class WeatherService:

    def __init__(self):
        pass

    @staticmethod
    def __get_weather(lng0, lat0, lng1, lat1):
        ds_weather = DarkSkyWeather()
        return ds_weather.get_year_weather(lng0, lat0, lng1, lat1)

    @staticmethod
    def __connect_weather_and_buildings(buildings, weather_net):

        def nearest_point(geometry, net):
            min_distance = 1000
            closest_point = {}
            for p in net:
                point = Point(p['coordinates'][0], p['coordinates'][1])
                distance = geometry.distance(point)
                if distance < min_distance:
                    min_distance = distance
                    closest_point = p

            return closest_point['response']

        def weather(row):
            weather_point = nearest_point(row['geometry'], weather_net)
            t = weather_point['temperature']
            c = weather_point['cloud_cover']
            h = weather_point['humidity']

            return t, c, h

        # import pdb; pdb.set_trace()
        buildings['temperature'], buildings['cloud_cover'], buildings['humidity'] =zip(*buildings.apply(weather, axis=1))
        # buildings['cloud_cover'] = b

        # (buildings['sum'], buildings['difference'], buildings['difference2']) = buildings.apply(
        #     lambda row: weather(row), axis=1)

        return buildings

    @staticmethod
    def enrich_buildings_with_weather(buildings, bottom_left, top_right):
        weather_net = WeatherService.__get_weather(
            bottom_left.x,
            bottom_left.y,
            top_right.x,
            top_right.y
        )

        buildings = WeatherService.__connect_weather_and_buildings(
            buildings,
            weather_net
        )

        return buildings


