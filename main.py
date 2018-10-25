from flask import Flask, request
from flask_pymongo import PyMongo

from config.mongo import MONGO_PORT, MONGO_DB
from utils.json_encoder import JSONEncoder
from services.building_service import BuildingService
from utils.custom_exceptions import ProcessingException
import traceback

app = Flask(__name__)

app.config['MONGO_URI'] = f"mongodb://localhost:{MONGO_PORT}/{MONGO_DB}"
# it works for me (Serhii) only when host: mongo
# app.config['MONGO_URI'] = f"mongodb://mongo:{MONGO_PORT}/{MONGO_DB}"


mongo = PyMongo(app)
app.json_encoder = JSONEncoder


@app.route('/processing', methods=['POST'])
def processing():
    try:
        data = request.get_json()
        building_service = BuildingService(mongo)
        buildings = building_service.get_buildings(data['bbox'])

        # TODO: buildings are ready to be shown as heatmap
        return str(buildings.count())
    except ProcessingException as exc:
        return "Custom exception: {0}".format(exc.message)
    except Exception as exc:
        return "System exception: {0}\r\nStack trace: {1}".format(exc, traceback.format_exc())


if __name__ == '__main__':
    app.run(port=8000, debug=True, host='0.0.0.0')
