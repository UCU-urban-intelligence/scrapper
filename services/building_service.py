from collections import namedtuple

from flask_pymongo import PyMongo
from flask_pymongo.wrappers import Collection
from scripts.buildings import DfCreator
from shapely import geometry
import json


Building = namedtuple('Building', ['addr_housenumber', 'addr_street', 'amenity', 'building', 'description', 'geometry', 'height', 'name', 'roof_shape'])


class BuildingService:
    __BUILDINGS_COLLECTION_NAME = 'buildings'
    __REQUEST_AREAS_COLLECTION_NAME = 'request-areas'

    def __init__(self, mongo: PyMongo):
        self.__request_areas: Collection = mongo.db[self.__REQUEST_AREAS_COLLECTION_NAME]
        self.__buildings: Collection = mongo.db[self.__BUILDINGS_COLLECTION_NAME]

    def __get_existing_bounds(self, bottom_left, top_right):
        for request_area in self.__request_areas.find():
            if (request_area.bottom_left.lat <= bottom_left[0] <= request_area.top_right.lat and
                    request_area.bottom_left.lng <= bottom_left[1] <= request_area.top_right.lng and
                    request_area.bottom_left.lat <= top_right[0] <= request_area.top_right.lat and
                    request_area.bottom_left.lng <= top_right[1] <= request_area.top_right.lng):
                return request_area

        return None

    def __save_buildings(self, buildings):
        buildings['geometry'] = buildings['geometry'].apply(geometry.mapping)
        result = self.__buildings.insert_many(buildings.to_dict('records'))


        #self.__buildings.insert()
        #self.__request_areas.insert()
        return buildings


    def __prepare_buildings(self, bottom_left, top_right):
        building_df_creator = DfCreator()
        buildings = building_df_creator.get_df(bottom_left[0], bottom_left[1], top_right[0], top_right[1])
        return buildings


    def get_buildings(self, bounds):
        bottom_left = [bounds[0], bounds[1]]
        top_right = [bounds[2], bounds[3]]

        existing_bounds = self.__get_existing_bounds(bottom_left, top_right)
        if existing_bounds:
            a = 5
        else:
            buildings = self.__prepare_buildings(bottom_left, top_right)
            self.__save_buildings(buildings)
        return None
