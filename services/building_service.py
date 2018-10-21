from flask_pymongo import PyMongo
from pymongo import GEOSPHERE
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

        # TODO: find appropriate place for index creation
        self.__buildings.create_index([("geometry", GEOSPHERE)])
        self.__buildings.create_index([("request_area_bottom_left", GEOSPHERE)])
        self.__buildings.create_index([("request_area_top_right", GEOSPHERE)])
        self.__request_areas.create_index([("bottom_left", GEOSPHERE)])
        self.__request_areas.create_index([("top_right", GEOSPHERE)])

    def __get_existing_bounds(self, bottom_left: Point, top_right: Point):
        # TODO: remove after $within will be fixed
        return None, None
        for request_area in self.__request_areas.find():
            existing_bottom_left = request_area['bottom_left']['coordinates']
            existing_top_right = request_area['top_right']['coordinates']
            if (existing_bottom_left[0] <= bottom_left.x <= existing_top_right[0] and
                    existing_bottom_left[1] <= bottom_left.y <= existing_top_right[1] and
                    existing_bottom_left[0] <= top_right.x <= existing_top_right[0] and
                    existing_bottom_left[1] <= top_right.y <= existing_top_right[1]):
                return (Point(existing_bottom_left[0], existing_bottom_left[1]),
                        Point(existing_top_right[0], existing_top_right[1]))

        return None, None

    def __save_buildings(self, buildings):
        result = self.__buildings.insert_many(buildings.to_dict('records'))
        return result

    def __save_request_area(self, bottom_left: Point, top_right: Point):
        request_area = {"bottom_left": geometry.mapping(bottom_left), "top_right": geometry.mapping(top_right)}
        result = self.__request_areas.insert(request_area)
        return result

    def __prepare_buildings(self, bottom_left: Point, top_right: Point):
        building_df_creator = BuildingsGetter()
        buildings = building_df_creator.get_df(bottom_left.x, bottom_left.y, top_right.x, top_right.y)
        buildings['geometry'] = buildings['geometry'].apply(geometry.mapping)
        buildings['request_area_bottom_left'] = bottom_left
        buildings['request_area_top_right'] = top_right
        buildings['request_area_bottom_left'] = buildings['request_area_bottom_left'].apply(geometry.mapping)
        buildings['request_area_top_right'] = buildings['request_area_top_right'].apply(geometry.mapping)
        return buildings

    def __get_buildings(self, existing_bottom_left: Point, existing_top_right: Point,
                        bottom_left: Point = None, top_right: Point = None):
        query = {"$and":
            [
                {'request_area_bottom_left.coordinates.0': existing_bottom_left.x},
                {'request_area_bottom_left.coordinates.1': existing_bottom_left.y},
                {'request_area_top_right.coordinates.0': existing_top_right.x},
                {'request_area_top_right.coordinates.1': existing_top_right.y}
            ]
        }

        # TODO: $within doesn't work
        if bottom_left and top_right and None:
            query = {"$and":
                [
                    {'request_area_bottom_left.coordinates.0': existing_bottom_left.x},
                    {'request_area_bottom_left.coordinates.1': existing_bottom_left.y},
                    {'request_area_top_right.coordinates.0': existing_top_right.x},
                    {'request_area_top_right.coordinates.1': existing_top_right.y},
                    {"geometry": {"$within":
                        {
                            "$box": [[bottom_left.x, bottom_left.y],
                                     [top_right.x, top_right.y]]
                        }}}
                ]
            }

        buildings = self.__buildings.find(query)

        return buildings

    def get_buildings(self, bounds):
        bottom_left = Point(bounds[0], bounds[1])
        top_right = Point(bounds[2], bounds[3])
        (existing_bottom_left, existing_top_right) = self.__get_existing_bounds(bottom_left, top_right)
        if existing_bottom_left and existing_top_right:
            buildings = self.__get_buildings(existing_bottom_left, existing_top_right, bottom_left, top_right)
        else:
            buildings = self.__prepare_buildings(bottom_left, top_right)
            self.__save_buildings(buildings)
            self.__save_request_area(bottom_left, top_right)
            buildings = self.__get_buildings(bottom_left, top_right)
        return buildings
