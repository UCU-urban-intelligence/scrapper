import sys
import logging

import overpy
import geopandas as gpd
from shapely import geometry


GEOM_COLUMN = 'geometry'
DEFAULT_HEIGHT = 15


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
    col_names = ['addr:housenumber', 'addr:street', 'amenity', 'building',
                 'description', 'geometry', 'height', 'name', 'roof:shape']

    num_cols = ['building:levels', 'height', 'building:height', 'roof:angle',
                'roof:height']

    @staticmethod
    def _get_nodes_points(nodes):
        " Return list of (lon, lat) for overpass nodes list"

        return [
            [float(node.lon), float(node.lat)] for node in nodes
        ]

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
                if row_data.get('building:height') is not None:
                    row_data['height'] = row_data['building:height']

                elif row_data.get('building:levels') is not None:
                    row_data['height'] = row_data['building:levels'] * 3 + 3

                else:
                    row_data['height'] = DEFAULT_HEIGHT

            if row_data.get('building') == 'yes':
                row_data['building'] = None

            row_data.update({
                GEOM_COLUMN: geometry.Polygon(outer_points, inner_points)
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

        return gpd.GeoDataFrame(
            ways_data + relations_data, columns=self.col_names,
            geometry=GEOM_COLUMN
        )


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

        return gpd.GeoDataFrame(data, geometry=GEOM_COLUMN)


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
