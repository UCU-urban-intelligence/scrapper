from flask_pymongo import PyMongo
from flask_pymongo.wrappers import Collection
from scripts.buildings import BuildingsGetter
from shapely import geometry
from shapely.geometry import Point


class BuildingService:
    __BUILDINGS_COLLECTION_NAME = 'buildings'
    __REQUEST_AREAS_COLLECTION_NAME = 'request-areas'

    def __init__(self, mongo: PyMongo):
        self.__request_areas: Collection = mongo.db[self.__REQUEST_AREAS_COLLECTION_NAME]
        self.__buildings: Collection = mongo.db[self.__BUILDINGS_COLLECTION_NAME]

    def __get_existing_bounds(self, bottom_left: Point, top_right: Point):
        for request_area in self.__request_areas.find():
            if (request_area.bottom_left.lat <= bottom_left.x <= request_area.top_right.lat and
                    request_area.bottom_left.lng <= bottom_left.y <= request_area.top_right.lng and
                    request_area.bottom_left.lat <= top_right.x <= request_area.top_right.lat and
                    request_area.bottom_left.lng <= top_right.y <= request_area.top_right.lng):
                return request_area

        return None


    def __save_buildings(self, buildings):
        result = self.__buildings.insert_many(buildings.to_dict('records'))
        return result


    def __save_request_area(self, bottom_left: Point, top_right: Point):
        dict = {"bottom_left" : geometry.mapping(bottom_left), "top_right" : geometry.mapping(top_right) }
        result = self.__request_areas.insert(dict)
        return result


    def __prepare_buildings(self, bottom_left: Point, top_right: Point):
        building_df_creator = BuildingsGetter()
        buildings = building_df_creator.get_df(bottom_left.x, bottom_left.y, top_right.x, top_right.y)
        buildings['geometry'] = buildings['geometry'].apply(geometry.mapping)
        return buildings


    def get_buildings(self, bounds):
        bottom_left = Point(bounds[0], bounds[1])
        top_right = Point(bounds[2], bounds[3])

        existing_bounds = self.__get_existing_bounds(bottom_left, top_right)
        if existing_bounds:
            return None
        else:
            buildings = self.__prepare_buildings(bottom_left, top_right)
            self.__save_buildings(buildings)
            self.__save_request_area(bottom_left, top_right)
            return buildings
