# yfpy/data_processor.py
import pandas as pd


# def extract_data(weekly_data, cumulative_data, all_data):
#    extracted_data = []
#    if isinstance(weekly_data, dict) and 'matchups' in weekly_data:
#        for matchup in weekly_data['matchups']:
#            # Your existing extraction logic here
#            pass
#    return pd.DataFrame(extracted_data)


def extract_data(weekly_data, cumulative_data, all_data):
    # For now, simply return the weekly_data to check if it is received correctly
    return weekly_data
