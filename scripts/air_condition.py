import sys
import requests


class AirCondition:
    """
        For more info about API go here:
        https://breezometer.com/air-quality-api/
    """

    API_PATH = "https://api.breezometer.com/baqi/"

    API_KEY = "194734dfed444b2b97e397498e434a85"

    def __init__(self):
        pass

    def get_df(self, lat1, lng1, lat2, lng2):
        print(lat1, lng1, lat2, lng2)
        mean_lat = (lat1 + lat2) / 2
        mean_lng = (lng1 + lng2) / 2
        print({"mean_lat": mean_lat, "mean_lng": mean_lng})

        response = requests.get(
            AirCondition.API_PATH,
            [
                ("lat", "{:.3f}".format(round(mean_lat, 3))),
                ("lon", "{:.3f}".format(round(mean_lng, 3))),
                ("key", AirCondition.API_KEY)
            ]
        )
        return response.text


if __name__ == '__main__':
    ac = AirCondition()
    bbox = map(float, sys.argv[1:])

    result = ac.get_df(*bbox)

    with open('out.json', 'w') as f:
        f.write(str(result))
