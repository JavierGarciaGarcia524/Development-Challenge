from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
import traceback

class Weather_Utils:
    @staticmethod
    def format_aemet_date(dt: datetime) -> str:
        return dt.strftime("%Y-%m-%dT%H:%M:%SUTC")

    """ FUNCTION TO PROCESS AEMET DATA WHEN OBTAINED THROUGH THE API. VALIDATE, SELECT, AND AGGREGATE DATA ACCORDING TO USER REQUIREMENTS """
    @staticmethod
    def process_aemet_data(weather_data, desired_features, aggregation_value):
        time_zone='UTC'
        # Data validation
        if not weather_data or not isinstance(weather_data, (list, dict)):
            print("Error: Invalid or empty input data")
            return None
    
        try:
            df = pd.DataFrame(weather_data)
           
            # Verification of the hour column
            if 'fhora' not in df.columns:
                print("Error: The data does not contain the 'fhora' column")
                return None
            
            # Select only the required columns, reduce the dataset
            cols_to_keep = ['fhora', 'nombre', 'temp', 'pres', 'vel']
            for col in cols_to_keep:
                if col not in df.columns:
                    df[col] = pd.NA  # Create the column if missing
            df = df[cols_to_keep]
            
            # Date processing
            df['fhora'] = pd.to_datetime(df['fhora'], utc=True)          # Parse UTC
            df['fhora'] = df['fhora'].dt.tz_convert('Europe/Madrid')     # Convert Madrid
            
            """ 
            Trying column selection, delete later
            """
            # 1.- Select columns
            df = Weather_Utils.column_selection(df, desired_features)
            # 2.- Temporal aggregation
            df = Weather_Utils.aggregate_weather_data(df, aggregation_value)
            # 3.- Define index & order
            df = df.sort_values('fhora').reset_index(drop=True)
            if pd.api.types.is_datetime64_any_dtype(df['fhora']):
                df['fhora'] = df['fhora'].dt.strftime('%Y-%m-%dT%H:%M:%S%z')

            # df = df.set_index('fhora').sort_index()
            # df.index.name = 'fhora'
            return df

        except Exception as e:
            print(f"Error processing data: {str(e)}")
            traceback.print_exc()
            # Debugging information
            print("Weather data content:", weather_data)
            print("Detected columns:", getattr(df, "columns", None))
            return None


    """ FUNCTION TO SELECT COLUMNS SELECTED BY USER """
    @staticmethod
    def column_selection(weather_data, desired_features):
        mandatory_cols = ['fhora', 'nombre']
        missing_mandatory = [col for col in mandatory_cols if col not in weather_data.columns]
        # Validate structure
        if missing_mandatory:
            raise ValueError(f"Dataframe is incomplete: {missing_mandatory}")
        # If no feature was selected, we return them all
        if not desired_features:
            return weather_data
        # Obtain possible columns in the selected ones
        available_features = [col for col in desired_features if col in weather_data.columns]
        selected_cols = mandatory_cols + available_features
        return weather_data[selected_cols]

    """ FUNCTION TO AGGREGATE WEATHER DATA """
    @staticmethod
    def aggregate_weather_data(weather_data, aggregation_value):
        # Double check data exists
        if weather_data is None or not isinstance(weather_data, pd.DataFrame) or weather_data.empty:
            print("Error: No data to aggregate")
            return None
        # Validate aggregation
        allowed_values = [None, 'hourly', 'daily', 'monthly']
        if aggregation_value not in allowed_values:
            raise ValueError(f"Aggregation '{aggregation_value}' not supported. Choose from ['hourly', 'daily', 'monthly'] or None.")
        # Perform aggregation
        if aggregation_value is None:
            return weather_data
        freq_map = {
            'hourly': 'h',
            'daily': 'd',
            'monthly': 'MS'
        }
        possible_numeric_cols=['temp', 'pres', 'vel']
        numeric_cols = [col for col in possible_numeric_cols if col in weather_data.columns]
        
        for col in numeric_cols:
            weather_data[col] = pd.to_numeric(weather_data[col], errors='coerce')
                  
        # Group and calc mean for only selected features
        grouped = weather_data.groupby(['nombre', pd.Grouper(key='fhora', freq=freq_map[aggregation_value.lower()])])
        result = grouped[numeric_cols].mean().reset_index()
        
        if aggregation_value == 'monthly':
            result['fhora'] = result['fhora'].dt.tz_convert('Europe/Madrid')    # Double check

        # print(result.head(5))
        return result
    
    """ FUNCTION TO OBTAIN EQUIVALENCE FROM MADRID DAYS TO UTC TIME """
    @staticmethod
    def madrid_dates_to_aemet_utc(init_date, end_date):
        
        init_madrid = datetime.fromisoformat(init_date + "T00:00:00").replace(tzinfo=ZoneInfo("Europe/Madrid"))
        end_madrid  = datetime.fromisoformat(end_date + "T23:59:59").replace(tzinfo=ZoneInfo("Europe/Madrid"))

        init_utc = init_madrid.astimezone(ZoneInfo("UTC"))
        end_utc  = end_madrid.astimezone(ZoneInfo("UTC"))

        init_str = init_utc.strftime("%Y-%m-%dT%H:%M:%S") + "UTC"
        end_str  = end_utc.strftime("%Y-%m-%dT%H:%M:%S") + "UTC"

        return init_str, end_str