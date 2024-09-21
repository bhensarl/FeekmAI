# yfpy/division_table_gen.py
# -*- coding: utf-8 -*-
"""YFPY demo."""

__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import os
import sys
import pandas as pd
import time  # Import time module for delays
import json

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

chosen_week = 1  # Set the week number to query

# Sample matchups data (already a Python object)
matchups = yahoo_query.get_league_matchups_by_week(chosen_week)

# Set the total number of weeks in the fantasy season (adjust as needed)
total_weeks = 17  # You can adjust this number based on your league's season length

# Initialize lists to store data for all weeks
match_ids = []
season_ids = []
week_numbers = []
home_team_ids = []
away_team_ids = []
home_team_actual_points = []
away_team_actual_points = []
home_team_projected_points = []
away_team_projected_points = []

# Loop through all weeks
for week in range(1, total_weeks + 1):
    # Query the matchups data for the current week
    matchups = yahoo_query.get_league_matchups_by_week(week)

    # Extract data from matchups (iterating through Matchup objects)
    for matchup in matchups:
        # Assuming a unique match_id can be the combination of the involved team IDs
        match_id = f"{matchup.teams[0].team_id}_vs_{matchup.teams[1].team_id}"
        
        season_id = season  # Use the season variable you have defined earlier
        week_number = matchup.week  # Use dot notation to access attributes

        # Extract home and away team data
        home_team = matchup.teams[0]  # First team as home team
        away_team = matchup.teams[1]  # Second team as away team

        # Append match details
        match_ids.append(match_id)
        season_ids.append(season_id)
        week_numbers.append(week_number)
        home_team_ids.append(home_team.team_id)
        away_team_ids.append(away_team.team_id)
        home_team_actual_points.append(home_team.team_points.total)
        away_team_actual_points.append(away_team.team_points.total)
        home_team_projected_points.append(home_team.team_projected_points.total)
        away_team_projected_points.append(away_team.team_projected_points.total)

# Create a DataFrame with all the extracted data and name it df_matchups
df_matchups = pd.DataFrame({
    'Match ID': match_ids,
    'Season ID': season_ids,
    'Week Number': week_numbers,
    'Home Team ID': home_team_ids,
    'Away Team ID': away_team_ids,
    'Home Team Actual Points': home_team_actual_points,
    'Away Team Actual Points': away_team_actual_points,
    'Home Team Projected Points': home_team_projected_points,
    'Away Team Projected Points': away_team_projected_points,
})

# Display the df_matchups DataFrame
print(df_matchups)

# Save the DataFrame to a CSV file
csv_output_path = data_dir / "matchups_all_weeks.csv"
df_matchups.to_csv(csv_output_path, index=False)
