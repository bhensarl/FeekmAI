import pandas as pd
from pandas import json_normalize

def load_weekly_data(json_data):
    try:
        # Check if json_data is a string and parse it
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data
        
        # Flatten the JSON structure
        if isinstance(data, dict):
            if 'matchups' in data:
                flat_data = json_normalize(data['matchups'], sep='_')
                return flat_data
            else:
                print("No 'matchups' key found in the dictionary", file=sys.stderr)
                return pd.DataFrame()  # Return an empty DataFrame if key is missing
        elif isinstance(data, list):
            flat_data = json_normalize(data, sep='_')
            return flat_data

        print("Unexpected data format", file=sys.stderr)
        return pd.DataFrame()  # Return an empty DataFrame for unexpected format

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}", file=sys.stderr)
        return pd.DataFrame()  # Return an empty DataFrame
