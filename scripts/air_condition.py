import sys
import requests
from random import randint
from utils import create_net
import json


class AirCondition:
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

    def __init__(self):
        pass

    def get_df(self, lat1, lng1, lat2, lng2):
        print(lat1, lng1, lat2, lng2)
        net = create_net(lat1, lng1, lat2, lng2, 0.1)

        result = []
        for coordinates in net:
            print(coordinates)
            api_key_for_request = AirCondition.API_KEYS[randint(0, len(AirCondition.API_KEYS) - 1)]

            response = requests.get(
                AirCondition.API_PATH,
                [
                    ("lat", coordinates[0]),
                    ("lon", coordinates[1]),
                    ("key", api_key_for_request),
                    ("fields", "breezometer_aqi")
                ]
            )

            result.append({
                "coordinates": [coordinates[0], coordinates[1]],
                "response": json.loads(response.text)
            })

        return result


if __name__ == '__main__':
    ac = AirCondition()
    bbox = map(float, sys.argv[1:])

    result = ac.get_df(*bbox)

    with open('out.json', 'w') as f:
        r = json.dumps(result)
        f.write(str(r))
