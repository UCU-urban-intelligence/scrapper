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

        def weather(geometry):
            weather_point = nearest_point(geometry, weather_net)
            return weather_point

        buildings['weather'] = buildings['geometry'].apply(weather)

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


