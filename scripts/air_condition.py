import requests


class DfCreator:
    """
        For more info about API go here:
        https://aqicn.org/json-api/doc/#api-Geolocalized_Feed
    """

    API_PATH = "https://api.waqi.info/feed/"
    PRIVATE_API_TOKEN = "a480e8757e5d667d81053f4a143146f32b9ed8b2"

    def __init__(self):
        pass

    def get_df(self, lat1, lng1, lat2, lng2):
        mean_lat = (lat1 + lat2) / 2
        mean_lng = (lng1 + lng2) / 2
        # geo::lat;:lng/?token=:token
        response = requests.get(
            DfCreator.API_PATH + "/geo{};{}/".format(mean_lat, mean_lng),
            [("token", DfCreator.PRIVATE_API_TOKEN)]
        )
        print(response.status_code)
        return response.text
