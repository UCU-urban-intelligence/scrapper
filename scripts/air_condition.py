import sys
import requests
from random import randint
from utils.net import create_net, net_by_quantity
from shapely import geometry
import geopandas as gpd
import json

GEOM_COLUMN = 'geometry'


class AirConditionGetter:
    """
        For more info about API go here:
        https://breezometer.com/air-quality-api/
    """

    API_PATH = "https://api.breezometer.com/baqi/"

    API_KEYS = [
        "44454c79cdcb4a409f0f852f76b22c54",
        "194734dfed444b2b97e397498e434a85",
        "441aacba5c4f4c2385b74483bd59a8ec",
        "60babde2ae614606bb60623843867136",
        "186a594cfae44136b7ce52bddac4b4a7"
    ]

    NET_STEP = 0.01
    MAX_QTY = 36

    def get_df(self, lng1, lat1, lng2, lat2):
        net = create_net(lng1, lat1, lng2, lat2, self.NET_STEP)
        if len(net) > self.MAX_QTY:
            net = net_by_quantity(lng1, lat1, lng2, lat2, self.MAX_QTY)
        data = []
        for coordinates in net:
            api_key_for_request = AirConditionGetter.API_KEYS[randint(0, len(AirConditionGetter.API_KEYS) - 1)]

            response = requests.get(
                AirConditionGetter.API_PATH,
                [
                    ("lon", coordinates[0]),
                    ("lat", coordinates[1]),
                    ("key", api_key_for_request),
                    ("fields", "breezometer_aqi")
                ]
            )

            data.append({
                GEOM_COLUMN: geometry.Point(coordinates[0], coordinates[1]),
                "aqi": json.loads(response.text)['breezometer_aqi']
            })

        return gpd.GeoDataFrame(data, geometry=GEOM_COLUMN)


if __name__ == '__main__':
    ac = AirConditionGetter()
    bbox = map(float, sys.argv[1:])

    result = ac.get_df(*bbox)

    with open('out.json', 'w') as f:
        r = json.dumps(result)
        f.write(str(r))
