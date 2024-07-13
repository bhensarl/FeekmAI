# yfpy/data_loader.py
import json


def load_weekly_data(week_number):
    file_path = f'scores/week{week_number}.json'
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        data = {}
    if isinstance(data, list):
        data = data[0] if data else {}
    return data
