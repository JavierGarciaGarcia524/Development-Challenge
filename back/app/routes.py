from flask import Blueprint, request, jsonify
import os
from .services.aemet_service import AEMET_Client
from .services.weather_utils import Weather_Utils

api_blueprint = Blueprint('api', __name__)

aemet_client = AEMET_Client(api_key = os.getenv('AEMET_API_KEY'))
weather_utils = Weather_Utils()

@api_blueprint.route('/')
def home():
    return "¡Working!"

@api_blueprint.route('/weather', methods=['GET'])
def get_weather():
    station = request.args.get('station')
    init_date = request.args.get('init_date')
    end_date = request.args.get('end_date')
    desired_features = request.args.getlist('desired_features[]')       # list
    aggregation_value = request.args.get('aggregation_value', None)     # default None
    
    if not station or not init_date or not end_date:
        return jsonify({"error": "Missing basic parameters, init_date, end_date"}), 400
    
    raw_data = aemet_client.get_weather_data(
        f"{init_date}T00:00:00UTC",
        f"{end_date}T23:59:59UTC",
        station
    )
    
    if raw_data is None:
        return jsonify({"error": "No data available or an error occurred"}), 500
    
    df = weather_utils.process_aemet_data(raw_data, desired_features, aggregation_value)

    if df is None:
        return jsonify({"error": "Data processing error"}), 500

    return jsonify(df.reset_index().to_dict(orient="records"))
