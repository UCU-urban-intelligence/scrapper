import sys
import requests


class AirCondition:
    """
        For more info about API go here:
        https://aqicn.org/json-api/doc/#api-Geolocalized_Feed
        
        Test data:
        https://wiki.openstreetmap.org/wiki/Bounding_Box
        "boundingbox":["51.2867602","51.6918741","-0.5103751","0.3340155"]
    """

    API_PATH = "https://api.waqi.info/feed/"
    PRIVATE_API_TOKEN = "a480e8757e5d667d81053f4a143146f32b9ed8b2"

    def __init__(self):
        pass

    def get_df(self, lat1, lng1, lat2, lng2):
        print(lat1, lat2, lng1, lng2)
        mean_lat = (lat1 + lng1) / 2
        mean_lng = (lat2 + lng2) / 2
        print({"mean_lat": mean_lat, "mean_lng": mean_lng})
        response = requests.get(
            AirCondition.API_PATH + "/geo:{};{}/".format(mean_lat, mean_lng),
            [("token", AirCondition.PRIVATE_API_TOKEN)]
        )
        return response.text


if __name__ == '__main__':
    ac = AirCondition()
    bbox = map(float, sys.argv[1:])

    result = ac.get_df(*bbox)

    with open('out.json', 'w') as f:
        f.write(str(result))
