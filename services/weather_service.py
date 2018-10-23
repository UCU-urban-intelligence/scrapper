from flask_pymongo import PyMongo
from flask_pymongo.wrappers import Collection
from scripts.weather import DarkSkyWeather
from utils.nearest_point import find_nearest_point


class WeatherService:
    __BUILDINGS_COLLECTION_NAME = 'buildings'

    def __init__(self, mongo: PyMongo):
        self.__buildings: Collection = mongo.db[self.__BUILDINGS_COLLECTION_NAME]

    def __get_weather(self, lat0, lng0, lat1, lng1):
        ds_weather = DarkSkyWeather()
        return ds_weather.get_year_weather(lat0, lng0, lat1, lng1)

    def __connect_weather_and_buildings(self, weather_net, buildings, bbox):
        for building in buildings:
            point = find_nearest_point(weather_net, building)
            self.__buildings.update_one({'_id': building['_id']}, {'$set': point['response']})


    def assign_weather(self, bbox, buildings=[]):
        w_data = self.__get_weather(bbox[0], bbox[1], bbox[2], bbox[3])

        # TODO: replace with buildings from building_service when it works
        # buildings = self.__buildings.find({})

        self.__connect_weather_and_buildings(w_data, buildings, bbox)


