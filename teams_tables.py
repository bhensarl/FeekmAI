# yfpy/teams_tables.py
# -*- coding: utf-8 -*-
"""YFPY demo."""

__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import os
import sys
import pandas as pd

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


def clean_team_name(name):
    """Function to clean up the team names by decoding byte-like strings and removing unnecessary characters."""
    if isinstance(name, bytes):
        # Decode byte string to normal string
        name = name.decode('utf-8', errors='replace')  # 'replace' to handle decoding errors gracefully
    return name.strip()  # Remove any leading/trailing spaces or quotes


# Create an empty list to hold team data for all years
all_years_team_data = []

for year, ids in combined_ids.items():
    print(f"Processing year: {year}")
    # Update game_id and league_id for the current year
    game_id = ids["game_id"]
    league_id = ids["league_id"]

    try:
        # Generate teams database using YahooFantasySportsQuery for the current year
        yahoo_query = YahooFantasySportsQuery(
            auth_dir,
            league_id,
            game_id,
            offline=False,
            all_output_as_json_str=False,
            consumer_key=os.environ["YFPY_CONSUMER_KEY"],
            consumer_secret=os.environ["YFPY_CONSUMER_SECRET"]
        )

        teams = yahoo_query.get_league_teams()

        print(f"Number of teams retrieved for {year}: {len(teams)}")

        # Process teams for the current year
        for team in teams:
            try:
                team_id = int(team.team_id)
                team_name = clean_team_name(team.name)
                owner_name = team.managers[0].nickname if team.managers else "Unknown"
                division_id = team.division_id if hasattr(team, 'division_id') else None

                # Append the team data as a dictionary to the list
                all_years_team_data.append({
                    "year": year,
                    "team_id": team_id,
                    "owner_name": owner_name,
                    "team_name": team_name,
                    "division_id": division_id,
                })
                print(f"Added team: {team_name} for year {year}")
            except Exception as e:
                print(f"Error processing team in {year}: {str(e)}")

    except Exception as e:
        print(f"Error retrieving teams for {year}: {str(e)}")

print(f"Total number of teams processed: {len(all_years_team_data)}")

# Convert the list of dictionaries into a Pandas DataFrame
teams_df = pd.DataFrame(all_years_team_data)

# Display the DataFrame to ensure it's correctly formatted
print(teams_df)

if teams_df.empty:
    print("DataFrame is empty. No data was successfully processed.")
else:
    # Save the DataFrame to a CSV file
    csv_output_path = data_dir / "teams_all_years.csv"
    teams_df.to_csv(csv_output_path, index=False)
    print(f"Data saved to {csv_output_path}")


# Function to clean extra characters from team names
def clean_team_name(name):
    """Function to clean up the team names by decoding byte-like strings and removing unnecessary characters."""
    if isinstance(name, bytes):
        # Decode byte string to normal string
        name = name.decode('utf-8', errors='replace')  # 'replace' to handle decoding errors gracefully
    return name.strip()  # Remove any leading/trailing spaces or quotes
