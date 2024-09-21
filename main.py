# yfpy/main.py
# -*- coding: utf-8 -*-
"""YFPY demo."""

__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import os
import sys
import pandas as pd
import time  # Import time module for delays
import re

# from logging import DEBUG
from pathlib import Path
from datetime import datetime  # Import datetime for timestamp of csv file
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


def clean_team_name(team_name):
    if isinstance(team_name, bytes):
        team_name = team_name.decode('utf-8')  # Decode byte string to regular string
    # Use regex to strip out emojis and unwanted characters (like the b'' encoding)
    cleaned_name = re.sub(r'[^\w\s\'#-]', '', team_name).strip()
    return cleaned_name


def fetch_team_divisions(yahoo_query):
    """Fetch team division data from the league and return a dictionary with team_key as key and division as value."""
    team_divisions = {}
    try:
        teams = yahoo_query.get_league_teams()
        for team in teams:
            team_key = team.team_key
            # If the team has a division attribute, capture it; otherwise, set to 'No Division'
            team_division = getattr(team, 'division', {}).get('name', 'No Division')
            team_divisions[team_key] = team_division
    except Exception as e:
        print(f"Error fetching team divisions: {e}")
    return team_divisions


def process_scoreboard_to_dataframe(scoreboard, year, team_divisions):
    """Process scoreboard and merge division data into the standings DataFrame."""
    # Initialize a list to hold matchup data
    matchup_data = []

    # Check if 'matchups' exist in the scoreboard
    if not hasattr(scoreboard, 'matchups') or not scoreboard.matchups:
        print("No matchups found in the scoreboard data.")
        return pd.DataFrame()

    # Iterate over the matchups in the scoreboard
    for matchup in scoreboard.matchups:
        # Each matchup has teams
        teams = matchup.teams
        if len(teams) < 2:
            continue  # Skip incomplete matchups

        # Extract data for each team
        for i in range(len(teams)):
            team = teams[i]
            opponent = teams[1 - i] if len(teams) > 1 else None

            # Get division for both teams
            team_division = team_divisions.get(team.team_key, 'No Division')
            opponent_division = team_divisions.get(opponent.team_key, 'No Division') if opponent else 'No Division'

            team_data = {
                'Team_Key': team.team_key,
                'Team_Name': clean_team_name(team.name),
                'Division': team_division,  # Add division here
                'Points': getattr(team.team_points, 'total', 0),
                'Week': matchup.week,
                'Year': year,  # Set the Year explicitly
                'Opponent_Team_Key': opponent.team_key if opponent else '',
                'Opponent_Team_Name': clean_team_name(opponent.name) if opponent else '',
                'Opponent_Division': opponent_division,  # Add opponent division here
                'Opponent_Points': getattr(opponent.team_points, 'total', 0) if opponent else 0
            }

            # Append team data to the list
            matchup_data.append(team_data)

    # Convert the list of dictionaries to a DataFrame
    standings = pd.DataFrame(matchup_data)
    return standings


def fetch_and_combine_standings(auth_dir, game_code):
    # Initialize an empty DataFrame to store complete standings
    standings_complete = pd.DataFrame()

    # Set default start and end weeks
    start_week = 1
    end_week = 17

    for year, ids in combined_ids.items():
        league_id = ids["league_id"]
        game_id = ids["game_id"]

        print(f"Processing Year: {year}")
        try:
            # Initialize the YahooFantasySportsQuery object for the current year
            yahoo_query = YahooFantasySportsQuery(
                auth_dir,
                league_id,
                game_id,
                offline=False,
                all_output_as_json_str=False,
                consumer_key=os.environ["YFPY_CONSUMER_KEY"],
                consumer_secret=os.environ["YFPY_CONSUMER_SECRET"]
            )

            # Manually override league key
            yahoo_query.league_key = f"{game_id}.l.{league_id}"

            print(f"Year: {year}, Start Week: {start_week}, End Week: {end_week}")

            # Fetch team divisions
            team_divisions = fetch_team_divisions(yahoo_query)

        except Exception as e:
            print(f"Error fetching league settings or divisions for Year: {year}. Error: {e}")
            team_divisions = {}

        for week in range(start_week, end_week + 1):
            print(f"Processing Year: {year}, Week: {week}")
            try:
                # Fetch the scoreboard for the current week
                scoreboard = yahoo_query.get_league_scoreboard_by_week(week)

                # Improved error handling: Check if the scoreboard exists and contains matchups
                if not scoreboard or not hasattr(scoreboard, 'matchups') or not scoreboard.matchups:
                    print(f"No valid scoreboard data for Year: {year}, Week: {week}. Skipping this week.")
                    continue  # Skip to the next week if no data is found

                # Process the scoreboard data into a DataFrame
                standings = process_scoreboard_to_dataframe(scoreboard, year, team_divisions)

                # Check if standings DataFrame is empty
                if standings.empty:
                    print(f"No data to process for Year: {year}, Week: {week}.")
                    continue  # Skip to the next week

                # Append the standings to the complete standings DataFrame
                standings_complete = pd.concat([standings_complete, standings], ignore_index=True)

                # Respect API rate limits
                # time.sleep(1)  # Sleep for 1 second between requests

            except KeyError as e:
                print(f"KeyError: {e} for Year: {year}, Week: {week}. Skipping this week.")
                continue
            except Exception as e:
                print(f"An error occurred: {e} for Year: {year}, Week: {week}. Skipping this week.")
                continue

    return standings_complete




# Fetch and combine standings
standings_complete = fetch_and_combine_standings(auth_dir, game_code)

# Generate a timestamp for the filename
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# Create the output filename with the timestamp
output_filename = f'fantasy_football_standings_2018_2023_{timestamp}.csv'

# Save the complete standings DataFrame to a CSV file with the timestamped filename
standings_complete.to_csv(output_filename, index=False)

# Output the DataFrame
print(standings_complete)

#  Confirm that file was created
print(f"{output_filename} created successfully.")
