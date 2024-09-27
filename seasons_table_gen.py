# yfpy/seasons_table_gen.py
# -*- coding: utf-8 -*-
"""YFPY demo."""

__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import os
import sys
import pandas as pd
import time  # Import time module for delays

# from logging import DEBUG
from pathlib import Path
from dotenv import load_dotenv
from yfpy import Data
# from yfpy.logger import get_logger
from yfpy.query import YahooFantasySportsQuery
from variable_setup import (
    get_player_id,
    get_season,
    get_game_code,
    get_game_id,
    get_game_key,
    get_league_id,
    get_team_name
)

project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Load .env file to read local environment variables
load_dotenv(dotenv_path=project_dir / "auth" / ".env")

# Set directory location of private.json for authentication
auth_dir = project_dir / "auth"

# Set target directory for data output
data_dir = Path(__file__).parent / "output"

# Create YFPY Data instance for saving/loading data
data = Data(data_dir)

# Variables setup
season = get_season()
game_code = get_game_code()
game_id = get_game_id()
game_key = get_game_key()
league_id = get_league_id()
team_name = get_team_name()
player_id = get_player_id()

# Dictionary linking years to their respective league IDs and game IDs
combined_ids = {
    2018: {"game_id": 380, "league_id": "67583"},    # NFL - 2018
    2019: {"game_id": 390, "league_id": "43068"},    # NFL - 2019
    2020: {"game_id": 399, "league_id": "643103"},   # NFL - 2020
    2021: {"game_id": 406, "league_id": "333658"},   # NFL - 2021
    2022: {"game_id": 414, "league_id": "74941"},    # NFL - 2022
    2023: {"game_id": 423, "league_id": "219013"},   # NFL - 2023
}

# Generate teams database using YahooFantasySportsQuery
yahoo_query = YahooFantasySportsQuery(
    auth_dir,
    league_id,
    game_id,
    offline=False,
    all_output_as_json_str=False,
    consumer_key=os.environ["YFPY_CONSUMER_KEY"],
    consumer_secret=os.environ["YFPY_CONSUMER_SECRET"]
)
# Fetch league settings to determine valid weeks
league_settings = yahoo_query.get_league_settings()

# print(league_settings)

league_info = yahoo_query.get_league_info()
year = int(league_info.season)
# start_date = league_settings.start_date
# end_date = league_settings.end_date

# Initialize an empty list to store season data
season_data = []

# Example data (replace with actual data)
year = 2023
start_date = "2023-09-01"
end_date = "2024-01-01"

# Append the season data as a dictionary to the list
season_data.append({
    "year": year,
    "start_date": start_date,
    "end_date": end_date
})

# Convert the list of dictionaries to a DataFrame
df_seasons = pd.DataFrame(season_data)

# Optionally, print the DataFrame to verify the contents
print(df_seasons)

# Retrieve season_id (assuming season_id is the index)
df_seasons.reset_index(inplace=True)
df_seasons.rename(columns={'index': 'season_id'}, inplace=True)

# Optionally, print the DataFrame with season_id
print(df_seasons)

# Retrieve season_id for a specific year
season_id = df_seasons.loc[df_seasons['year'] == year, 'season_id'].values[0]
print(f"Season ID for year {year}: {season_id}")