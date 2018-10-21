from flask_pymongo import PyMongo
from scripts.buildings import DfCreator


class BuildingService:
    __BUILDINGS_COLLECTION_NAME = 'buildings'
    __REQUEST_AREAS_COLLECTION_NAME = 'request-areas'

    def __init__(self, mongo: PyMongo):
        self.__request_areas = mongo.db[self.__REQUEST_AREAS_COLLECTION_NAME]
        self.__buildings = mongo.db[self.__BUILDINGS_COLLECTION_NAME]

    def get_existing_bounds(self, bound_top_left, bound_bottom_right):
        for request_area in self.__request_areas.find():
            if (request_area.top_left.lat <= bound_top_left.lat <= request_area.bottom_right.lat and
                    request_area.top_left.lng <= bound_top_left.lng <= request_area.bottom_right.lng and
                    request_area.top_left.lat <= bound_bottom_right.lat <= request_area.bottom_right.lat and
                    request_area.top_left.lng <= bound_bottom_right.lng <= request_area.bottom_right.lng):
                return request_area

        return None

    def save_buildings(self, buildings):
        #self.__buildings.insert()
        #self.__request_areas.insert()
        return None

    def get_buildings(self, bound_top_left, bound_bottom_right, bound_top_left_search, bound_bottom_right_search):
        #self.__buildings.find()
        return None
