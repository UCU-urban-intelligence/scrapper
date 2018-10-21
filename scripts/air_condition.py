import sys
import requests
from random import randint


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
        mean_lat = (lat1 + lat2) / 2
        mean_lng = (lng1 + lng2) / 2
        print({"mean_lat": mean_lat, "mean_lng": mean_lng})

        api_key_for_request = AirCondition.API_KEYS[randint(0, len(AirCondition.API_KEYS) - 1)]

        response = requests.get(
            AirCondition.API_PATH,
            [
                ("lat", "{:.3f}".format(round(mean_lat, 3))),
                ("lon", "{:.3f}".format(round(mean_lng, 3))),
                ("key", api_key_for_request)
            ]
        )
        return response.text


if __name__ == '__main__':
    ac = AirCondition()
    bbox = map(float, sys.argv[1:])

    result = ac.get_df(*bbox)

    with open('out.json', 'w') as f:
        f.write(str(result))
