# yfpy/data_loader.py
import json
import sys
import os
import pandas as pd
from pandas import json_normalize


def load_weekly_data(season_number, week_number):
    file_path = f'scores/{season_number}/week{week_number}.json'

    # Error msg - file not found
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.", file=sys.stderr)
        return pd.DataFrame()  # Return an empty DataFrame

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            print("Loading data...")
            # print(f"Loaded data: {data}")  # Debugging statement prints data
            print(f"Data type: {type(data)}")  # Print the type of loaded data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}", file=sys.stderr)
        return pd.DataFrame()  # Return an empty DataFrame

    # Flatten the JSON structure
    if isinstance(data, dict):
        if 'matchups' in data:
            flat_data = json_normalize(data['matchups'], sep='_')
            # print(f"Flattened data: {flat_data}")  # Debugging statement
            return flat_data
        else:
            print(f"No 'matchups' key found in the dictionary from {file_path}", file=sys.stderr)
            return pd.DataFrame()  # Return an empty DataFrame if key is missing
    elif isinstance(data, list):
        flat_data = json_normalize(data, sep='_')
        return flat_data

    print(f"Unexpected data format in {file_path}", file=sys.stderr)
    return pd.DataFrame()  # Return an empty DataFrame for unexpected format
