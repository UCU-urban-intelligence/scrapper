import sys

import overpy
import geopandas as gpd
from shapely import geometry

OVERPASS_QUERY = """
(
    way["building"]({lat1}, {lng1}, {lat2}, {lng2});
    relation["building"]({lat1}, {lng1}, {lat2}, {lng2});
);

out body; >; out skel qt;
"""

COL_NAMES = ['addr:housenumber', 'addr:street', 'amenity', 'building',
             'building:levels', 'description', 'geometry', 'height', 'name',
             'roof:angle', 'roof:height', 'roof:levels', 'roof:material',
             'roof:orientation', 'roof:shape']

GEOM_COLUMN = 'geometry'


class DfCreator:

    def __init__(self):
        self.api = overpy.Overpass()
        self.ways_in_relations = set()

    @staticmethod
    def _get_nodes_points(nodes):
        " Return list of (lon, lat) for overpass nodes list"

        return [
            [float(node.lon), float(node.lat)] for node in nodes
        ]

    @staticmethod
    def _append_row_to_data(data, outer_points, inner_points=None, tags=None):
        """
         Create polygon using inner points and outer points. Append row to
         data list using this polygon and tags
        """

        # polygon need at least 3 points
        if outer_points and len(outer_points) > 2:
            row_data = tags.copy() if tags else {}

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
        ways_data = self._get_ways_data(result.ways)

        return gpd.GeoDataFrame(
            ways_data + relations_data, columns=COL_NAMES, geometry=GEOM_COLUMN
        )

    def get_df(self, lat1, lng1, lat2, lng2):

        query = OVERPASS_QUERY.format(
            lat1=lat1, lng1=lng1, lat2=lat2, lng2=lng2
        )

        result = self.api.query(query)

        return self._df_from_result(result)


if __name__ == '__main__':
    creator = DfCreator()
    bbox = map(float, sys.argv[1:])

    df = creator.get_df(*bbox)

    with open('out.geojson', 'w') as f:
        f.write(df.to_json())
