from flask import Blueprint, request, jsonify
import os
from .services.aemet_service import AEMET_Client
from .services.weather_utils import Weather_Utils
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
from zoneinfo import ZoneInfo

api_blueprint = Blueprint('api', __name__)

weather_utils = Weather_Utils()
aemet_client = AEMET_Client(api_key = os.getenv('AEMET_API_KEY'))

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

    # Im assuming I will implement the data selection as a calendar. For user to select graphically a range of days
    print(f"Received request for station: {station}, init_date: {init_date}, end_date: {end_date}, desired_features: {desired_features}, aggregation_value: {aggregation_value}")

    # Convert dates to Madrid timezone, enabling conversion to and obtaining the equivalent in UTC
    init_date_str, end_date_str = weather_utils.madrid_dates_to_aemet_utc(init_date, end_date)

    print(f"Converted dates to UTC timezone: init_date: {init_date_str}, end_date: {end_date_str}")

    raw_data = aemet_client.get_weather_data(
        init_date_str,
        end_date_str,
        station
    )

    if raw_data is None:
        return jsonify({"error": "No data available or an error occurred"}), 500
    
    df = weather_utils.process_aemet_data(raw_data, desired_features, aggregation_value)
    print(df.head(5))

    if df is None:
        return jsonify({"error": "Data processing error"}), 500

    return jsonify(df.reset_index().to_dict(orient="records"))
