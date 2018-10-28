import pyproj

import pickle
import pandas as pd
import logging
from flask_pymongo import PyMongo
from pymongo import GEOSPHERE
from flask_pymongo.wrappers import Collection

from sklearn.preprocessing import StandardScaler
from config.app import BBOX_AREA_RESTRICTION_SIZE
from scripts.air_condition import AirConditionGetter
from scripts.buildings import BuildingsGetter, ShopsGetter, WGS84_CRS
from services.weather_service import WeatherService
from shapely import geometry
from shapely.geometry import Point

from utils.custom_exceptions import ProcessingException

SHOPS_RADIUS = 500  # meters
CARTESIAN_CRS = {'init': 'epsg:3857'}
EQUAL_AREA_CRS = {'init': 'epsg:3035'}


class BuildingService:
    __BUILDINGS_COLLECTION_NAME = 'buildings'
    __REQUEST_AREAS_COLLECTION_NAME = 'request-areas'

    buildings_getter = BuildingsGetter()
    shops_getter = ShopsGetter()
    air_condition_getter = AirConditionGetter()

    def __init__(self, mongo: PyMongo):
        self.__request_areas: Collection = mongo.db[self.__REQUEST_AREAS_COLLECTION_NAME]
        self.__buildings: Collection = mongo.db[self.__BUILDINGS_COLLECTION_NAME]

        # TODO: find appropriate place for index creation
        self.__buildings.create_index([("geometry", GEOSPHERE)])
        self.__buildings.create_index([("request_area_bottom_left", GEOSPHERE)])
        self.__buildings.create_index([("request_area_top_right", GEOSPHERE)])
        self.__request_areas.create_index([("bottom_left", GEOSPHERE)])
        self.__request_areas.create_index([("top_right", GEOSPHERE)])
        self.__buildings.create_index([("building_centroid", GEOSPHERE)])

    def __get_existing_bounds(self, bottom_left: Point, top_right: Point):
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

    def __mapToGeoJson(self, buildings):
        buildings['geometry'] = buildings['geometry'].apply(geometry.mapping)
        buildings['request_area_bottom_left'] = buildings['request_area_bottom_left'].apply(geometry.mapping)
        buildings['request_area_top_right'] = buildings['request_area_top_right'].apply(geometry.mapping)
        buildings['building_centroid'] = buildings['building_centroid'].apply(geometry.mapping)
        return buildings

    def __save_buildings(self, buildings):
        buildings = self.__mapToGeoJson(buildings)
        result = self.__buildings.insert_many(buildings.to_dict('records'))
        return result

    def __save_request_area(self, bottom_left: Point, top_right: Point):
        request_area = {"bottom_left": geometry.mapping(bottom_left), "top_right": geometry.mapping(top_right)}
        result = self.__request_areas.insert(request_area)
        return result

    def __preProcessBuildings(self, buildings, bottom_left: Point, top_right: Point, bbox_id=""):
        buildings['building_centroid'] = buildings['geometry'].centroid
        buildings['request_area_bottom_left'] = bottom_left
        buildings['request_area_top_right'] = top_right
        buildings['bbox_id'] = bbox_id

        return buildings

    def _enrich_buildings_with_area(self, buildings):
        cartesian_buildings = buildings['geometry'].to_crs(EQUAL_AREA_CRS)

        buildings['area'] = cartesian_buildings.apply(lambda x: x.area)

        return buildings

    def _enrich_buildings_with_shops(self, buildings, bottom_left, top_right):
        shops = self.shops_getter.get_df(
            bottom_left.x, bottom_left.y, top_right.x, top_right.y
        )

        if shops is None or shops.empty:
            buildings['closest_shop'] = 2  # very far
            buildings['shops_count'] = 0
            return buildings

        def get_shops(geometry):
            def distance(point):
                return point.distance(geometry)

            distances = shops['geometry'].apply(distance)

            closest_shop = int(distances.min())
            shops_amount = len(distances[distances < SHOPS_RADIUS])

            return {
                'closest_shop': closest_shop,
                'shops_amount': shops_amount
            }

        shops = shops.to_crs(CARTESIAN_CRS)
        centroids = buildings['geometry'].to_crs(CARTESIAN_CRS)\
            .apply(lambda x: x.centroid)

        logging.info('Created buildings in cartesian projection')

        new_columns = pd.DataFrame(list(centroids.apply(get_shops)))
        buildings[['closest_shop', 'shops_amount']] = \
            new_columns[['closest_shop', 'shops_amount']]

        return buildings

    def _enrich_buildings_with_air_condition(self, buildings, bottom_left, top_right):
        df = self.air_condition_getter.get_df(
            bottom_left.x, bottom_left.y, top_right.x, top_right.y
        )

        def closest_air_quality_point(geometry):
            def distance(point):
                return point.distance(geometry)
            df['distance'] = df['geometry'].apply(distance)
            min_dist_row = df.ix[df['distance'].idxmin()]
            return min_dist_row['aqi']

        buildings['air_quality'] = buildings['geometry'].apply(closest_air_quality_point)
        return buildings

    def __prepare_buildings(self, bottom_left: Point, top_right: Point, bbox_id=""):

        buildings = self.buildings_getter.get_df(
            bottom_left.x, bottom_left.y, top_right.x, top_right.y
        )

        if buildings.shape[0] == 0:
            raise ProcessingException("buildings are empty")

        buildings = self.__preProcessBuildings(
            buildings, bottom_left, top_right, bbox_id
        )

        logging.info('Started enrichment with shops')
        buildings = self._enrich_buildings_with_shops(
           buildings, bottom_left, top_right
        )

        logging.info('Started enrichment with area')
        buildings = self._enrich_buildings_with_area(buildings)

        logging.info('Started enrichment with air condiditon')

        buildings = self._enrich_buildings_with_air_condition(
            buildings, bottom_left, top_right
        )

        logging.info('Started enrichment with weather data')

        buildings = WeatherService.enrich_buildings_with_weather(
            buildings, bottom_left, top_right
        )

        out = buildings[['addr:housenumber', 'addr:street', 'type', 'geometry',
                         'height', 'name', 'area', 'closest_shop',
                         'shops_amount', 'roof_type', 'air_quality',
                         'temperature', 'cloud_cover', 'humidity']]

        loaded_model = pickle.load(open('./model/finalized_model.sav', 'rb'))

        sc = StandardScaler()
        X = out[
            ['air_quality', 'area', 'closest_shop',
             'cloud_cover', 'humidity', 'shops_amount', 'temperature',
             'flat_roof', 'gabled_roof', 'round_roof']]
        X = sc.fit_transform(X)

        y = loaded_model.predict(X)
        out['efficiency'] = y
        # In case of DB fault
        with open('out.geojson', 'w') as f:
            f.write(out.to_json())

        logging.info('Saved buildings to file')

        return buildings

    def __get_buildings(self, existing_bottom_left: Point, existing_top_right: Point,
                        bottom_left: Point = None, top_right: Point = None):

        if bottom_left and top_right:
            query = {"$and":
                [
                    {'request_area_bottom_left.coordinates.0': existing_bottom_left.x},
                    {'request_area_bottom_left.coordinates.1': existing_bottom_left.y},
                    {'request_area_top_right.coordinates.0': existing_top_right.x},
                    {'request_area_top_right.coordinates.1': existing_top_right.y},
                    {"geometry": {"$geoWithin":
                        {"$geometry": {
                            "type": "Polygon",
                            "coordinates": [[
                                [top_right.x, bottom_left.y],
                                [top_right.x, top_right.y],
                                [bottom_left.x, top_right.y],
                                [bottom_left.x, bottom_left.y],
                                [top_right.x, bottom_left.y]
                            ]]
                        }}}
                    }
                ]
            }
        else:
            query = {"$and":
                [
                    {'request_area_bottom_left.coordinates.0': existing_bottom_left.x},
                    {'request_area_bottom_left.coordinates.1': existing_bottom_left.y},
                    {'request_area_top_right.coordinates.0': existing_top_right.x},
                    {'request_area_top_right.coordinates.1': existing_top_right.y}
                ]
            }

        buildings = self.__buildings.find(query)

        return buildings

    def __bbox_validation(self, bottom_left: Point, top_right: Point):
            bottom_left_mx, bottom_left_my = pyproj.transform(pyproj.Proj(WGS84_CRS), pyproj.Proj(CARTESIAN_CRS), bottom_left.x, bottom_left.y)
            top_right_mx, top_right_my = pyproj.transform(pyproj.Proj(WGS84_CRS), pyproj.Proj(CARTESIAN_CRS), top_right.x, top_right.y)
            range_x = top_right_mx - bottom_left_mx
            range_y = top_right_my - bottom_left_my
            area = range_x * range_y

            if area > BBOX_AREA_RESTRICTION_SIZE:
                raise ProcessingException(
                    "Box is too big. Area must be <= {3:.2e} m^2\r\n"
                    "Currently x2 - x1 = {0:.2e} m\r\n"
                    "y2 - y1 = {1:.2e} m\r\n"
                    "Area = {2:.2e} m^2".format(range_x, range_y, area, BBOX_AREA_RESTRICTION_SIZE)
                )

    def get_buildings(self, data):
        bbox_id = data["id"] if "id" in data else ""
        bounds = data["bbox"]
        bottom_left = Point(bounds[0], bounds[1])
        top_right = Point(bounds[2], bounds[3])

        (existing_bottom_left, existing_top_right) = self.__get_existing_bounds(bottom_left, top_right)
        if existing_bottom_left and existing_top_right and False:
            buildings = self.__get_buildings(existing_bottom_left, existing_top_right, bottom_left, top_right)
        else:
            self.__bbox_validation(bottom_left, top_right)
            logging.info('Buildings was not found in db')
            buildings = self.__prepare_buildings(bottom_left, top_right, bbox_id)
            logging.info('Prepeared buildngs')

            self.__save_buildings(buildings)
            logging.info('Saved buildngs')

            self.__save_request_area(bottom_left, top_right)
            logging.info('Saved request_area')

            buildings = self.__get_buildings(bottom_left, top_right)
            logging.info('Got buildngs')
        return buildings
