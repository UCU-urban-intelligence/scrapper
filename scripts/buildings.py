import sys
import logging

import overpy
import geopandas as gpd
from shapely import geometry


GEOM_COLUMN = 'geometry'
DEFAULT_HEIGHT = 15

WGS84_CRS = {'init': 'epsg:4326'}

INAPPROPRIATE_TYPES = ['static_caravan', 'kiosk', 'religious', 'cathedral',
                       'chapel', 'church', 'mosque', 'temple', 'synagogue',
                       'shrine', 'bakehouse', 'stadium', 'train_station',
                       'grandstand', 'toilets', 'bridge', 'bunker', 'bunker',
                       'carport', 'conservatory', 'construction', 'cowshed',
                       'farm_auxiliary', 'garage', 'garages', 'garbage_shed',
                       'greenhouse', 'hangar', 'hut', 'roof', 'shed', 'sty',
                       'water_tower', 'ruins', 'transformer_tower', 'stable']


FLAT_ROOFS = ['flat', 'flat_with_terrace', 'flat_with_two_terraces',
              'flat_with_three_terraces', 'flat_with_four_terraces']

GABLED_ROOFS = ['gabled	gabled_height_moved', 'side_hipped', 'half_hipped',
                'hipped', 'pyramidal', 'double_skillion', 'triple_skillion',
                'diagonal_pass', 'diagonal_pass', 'saltbox', 'double_saltbox',
                'corner_saltbox', 'triple_saltbox', 'quadruple_saltbox',
                'gambrel', 'mansard_onesided', 'mansard', 'thai_cutted',
                'thai', 'pyramidal_diagonal', 'skilion_windmill',
                'double_gabled', 'basilical', 'cross_gabled',
                'basilical_five_aisled', 'apse_gabled', 'sawtoth', 'trapeze',
                'gabled_row', 'round_row', 'wave', 'equal_hipped',
                'equal_mansard', 'flat_mansard']

ROUND_ROOFS = ['round', 'round_pyramidal', 'round_skillion', 'round_gabled',
               'round_skillion_cutted', 'round_skillion_double_cutted',
               'round_hipped', 'dome', 'dome_overlapped', 'cone	mansard_cone',
               'double_mansard_cone', 'triple_mansard_cone', 'onion',
               'hyperbolic_paraboloid', 'parabolic', 'hyperbolic_tower',
               'elliptic_hyperboloid', 'ellipsoid_cutted',
               'elliptic_paraboloid', 'tent', 'geodesic_dome',
               'spherical_cutted']


class BaseOverpassGetter:
    query_template = '({});  out body; >; out skel qt;'

    def __init__(self):
        self.api = overpy.Overpass()
        self.ways_in_relations = set()
        self.query = self.query_template.format(self.base_query)

    def _df_from_result(result):
        raise NotImplementedError()

    def get_df(self, lon1, lat1, lon2, lat2):
        query = self.query.format(
            lat1=lat1, lon1=lon1, lat2=lat2, lon2=lon2
        )

        result = self.api.query(query)

        logging.info('Got response for {}, {}, {}, {}'.format(
            lon1, lat1, lon2, lat2
        ))

        df = self._df_from_result(result)

        logging.info('Created dataset for {}, {}, {}, {}'.format(
            lon1, lat1, lon2, lat2
        ))

        return df


class BuildingsGetter(BaseOverpassGetter):
    base_query = """
        way["building"]({lat1}, {lon1}, {lat2}, {lon2});
        relation["building"]({lat1}, {lon1}, {lat2}, {lon2});
    """
    col_names = ['addr:housenumber', 'addr:street', 'type', 'geometry',
                 'height', 'name', 'area', 'roof_type']

    num_cols = ['building:levels', 'height', 'building:height',
                'building:eaves:levels', 'building:eaves:height',
                'roof:height']

    @staticmethod
    def _get_nodes_points(nodes):
        " Return list of (lon, lat) for overpass nodes list"

        return [
            [float(node.lon), float(node.lat)] for node in nodes
        ]

    def _roof_type(self, row):
        if row.get('building') in INAPPROPRIATE_TYPES:
            return 'inappropriate'

        if row.get('roof:shape') in FLAT_ROOFS:
            return 'flat'

        if row.get('roof:shape') in GABLED_ROOFS or row.get('roof:ridge'):
            return 'gabled'

        if row.get('roof:shape') in ROUND_ROOFS:
            return 'round'

    def _append_row_to_data(self, data, outer_points, inner_points=None,
                            tags=None):
        """
         Create polygon using inner points and outer points. Append row to
         data list using this polygon and tags
        """

        # polygon need at least 3 points
        if outer_points and len(outer_points) > 2:
            row_data = tags.copy() if tags else {}

            for key in self.num_cols:
                if key in row_data:
                    split = row_data[key].split()
                    nums = [float(s) for s in split if s.isdigit()]

                    row_data[key] = nums[0] if nums else 0.0

            if row_data.get('height') is None:
                height = row_data.get('building:height',
                                      row_data.get('building:height'))

                levels = row_data.get('building:levels',
                                      row_data.get('building:eaves:levels'))

                roof_height = row_data.get('roof:height', 0)

                if levels and not height:
                    height = levels * 3

                elif not levels and not height:
                    height = DEFAULT_HEIGHT

                row_data['height'] = height + roof_height

            if row_data.get('building', 'yes') == 'yes':
                row_data['building'] = 'building'

            row_data['type'] = row_data.pop('building')

            try:
                polygon = geometry.Polygon(outer_points, inner_points)
            except Exception:
                return None

            row_data.update({
                GEOM_COLUMN: polygon,
                'roof_type': self._roof_type(row_data)
            })

            data.append(row_data)

    def _get_ways_data(self, ways):
        ways_data = []

        for way in ways:
            if way.id not in self.ways_in_relations:
                points = self._get_nodes_points(way.nodes)

                self._append_row_to_data(ways_data, points, tags=way.tags)

        return ways_data

    def _get_relations_data(self, relations):
        relations_data = []

        for rel in relations:
            outer_ways = [
                x.resolve() for x in rel.members if x.role == 'outer'
            ]

            inner_ways = [
                x.resolve() for x in rel.members if x.role == 'inner'
            ]

            if len(outer_ways) == 1:
                way = outer_ways[0]

                outer_points = self._get_nodes_points(way.nodes)

                inner_points = []

                for inner_way in inner_ways:
                    points = self._get_nodes_points(inner_way.nodes)
                    inner_points.append(points)

                    self.ways_in_relations.add(inner_way.id)

                self._append_row_to_data(
                    relations_data, outer_points, inner_points, tags=rel.tags
                )

                self.ways_in_relations.add(way.id)

            elif len(outer_ways) > 1:
                for way in outer_ways:
                    points = self._get_nodes_points(way.nodes)

                    self._append_row_to_data(
                        relations_data, points, tags=way.tags
                    )

                    self.ways_in_relations.add(way.id)

        return relations_data

    def _df_from_result(self, result):
        relations_data = self._get_relations_data(result.relations)
        logging.info('Processed relations data')

        ways_data = self._get_ways_data(result.ways)
        logging.info('Processed ways data')

        result = gpd.GeoDataFrame(
            ways_data + relations_data, columns=self.col_names,
            geometry=GEOM_COLUMN, crs=WGS84_CRS
        )

        result = self._modify_roof_types(result)

        return result

    def _modify_roof_types(self, df):
        df['inappropriate_type'] = df['roof_type'].map(
            lambda x: 1 if x == 'inappropriate' else 0
        )

        df['flat_roof'] = df['roof_type'].map(
            lambda x: 1 if x == 'flat' else 0
        )

        df['gabled_roof'] = df['roof_type'].map(
            lambda x: 1 if x == 'gabled' else 0
        )

        df['round_roof'] = df['roof_type'].map(
            lambda x: 1 if x == 'round' else 0
        )

        df.pop('roof_type')

        return df


class ShopsGetter(BaseOverpassGetter):
    base_query = """
        node["shop"="convenience"]({lat1}, {lon1}, {lat2}, {lon2});
        node["shop"="supermarket"]({lat1}, {lon1}, {lat2}, {lon2});
        node["amenity"="cafe"]({lat1}, {lon1}, {lat2}, {lon2});
        node["amenity"="fast_food"]({lat1}, {lon1}, {lat2}, {lon2});
        node["amenity"="restaurant"]({lat1}, {lon1}, {lat2}, {lon2});
    """

    def _df_from_result(self, result):
        data = []
        for node in result.nodes:
            row = {
                'type': node.tags.get('shop', node.tags.get('amenity')),
                'name': node.tags.get('name'),
                GEOM_COLUMN: geometry.Point(float(node.lon), float(node.lat))
            }

            data.append(row)

        return gpd.GeoDataFrame(data, geometry=GEOM_COLUMN, crs=WGS84_CRS) \
            if data else None


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)-15s | %(levelname)s | %(message)s'
)

if __name__ == '__main__':
    bbox = tuple(map(float, sys.argv[1:]))

    logging.info('Collecting buildings...')

    buildings_getter = BuildingsGetter()
    buildings_df = buildings_getter.get_df(*bbox)

    with open('buildings.geojson', 'w') as f:
        f.write(buildings_df.to_json())

    logging.info('Collecting shops...')

    shops_getter = ShopsGetter()
    shops_df = shops_getter.get_df(*bbox)

    with open('shops.geojson', 'w') as f:
        f.write(shops_df.to_json())
