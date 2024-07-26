# yfpy/main.py
# -*- coding: utf-8 -*-
"""YFPY demo.

"""
__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import os
import sys
import pandas as pd

from logging import DEBUG
from pathlib import Path
from dotenv import load_dotenv
# from test.integration.conftest import season, team_id
from yfpy import Data
from yfpy.logger import get_logger
from yfpy.query import YahooFantasySportsQuery
from variable_setup import get_season, get_game_code, get_game_id, get_game_key, get_league_id, get_team_name

project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

"""
Example public Yahoo league URL: "https://archive.fantasysports.yahoo.com/nfl/2014/729259"

Example vars using public Yahoo leagues still require auth through a personal Yahoo account: see README.md
"""

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ENVIRONMENT SETUP # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# load .env file in order to read local environment variables
load_dotenv(dotenv_path=project_dir / "auth" / ".env")

# set directory location of private.json for authentication
auth_dir = project_dir / "auth"

# set target directory for data output
data_dir = Path(__file__).parent / "output"

# create YFPY Data instance for saving/loading data
data = Data(data_dir)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# QUERY SETUP # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# from variable setup import located at top of file.  Adjust that if you want to pull additional variables.
season = get_season()
game_code = get_game_code()
game_id = get_game_id()
game_key = get_game_key()
league_id = get_league_id()
team_name = get_team_name()

# variables that change frequently
chosen_week = 1

# Dictionary linking years to their respective league IDs
# Combined dictionary for both game IDs and league IDs by year
combined_ids = {
    2018: {"game_id": 380, "league_id": "67583"},  # NFL - 2018
    2019: {"game_id": 390, "league_id": "43068"},  # NFL - 2019
    2020: {"game_id": 399, "league_id": "643103"},  # NFL - 2020
    2021: {"game_id": 406, "league_id": "333658"},  # NFL - 2021
    2022: {"game_id": 414, "league_id": "74941"},   # NFL - 2022
    2023: {"game_id": 423, "league_id": "219013"},  # NFL - 2023
}

def fetch_and_combine_standings(auth_dir, game_code):
    # Initialize an empty DataFrame to store complete standings
    standings_complete = pd.DataFrame()

    for year, ids in combined_ids.items():
        print(f"Processing year: {year}")  # Debug print to show the current year being processed
        print(f"Game ID: {ids['game_id']}, League ID: {ids['league_id']}")
        
        league_id = ids["league_id"]
        game_id = ids["game_id"]  # Use the game_id from the combined_ids dictionary

        # Print the game_id and league_id to debug
        print(f"Debug: Year: {year}, Game ID: {game_id}, League ID: {league_id}")

        # Initialize the YahooFantasySportsQuery object for the current year
        yahoo_query = YahooFantasySportsQuery(
            auth_dir,
            league_id,
            game_id,
            chosen_week,
            offline=False,
            all_output_as_json_str=False,
            consumer_key=os.environ["YFPY_CONSUMER_KEY"],
            consumer_secret=os.environ["YFPY_CONSUMER_SECRET"]
        )

        # Fetch the standings for the current year
        standings = yahoo_query.get_league_standings()
        print(standings)
        # Add a column to the standings DataFrame to indicate the year
        # standings['Year'] = year

        # Append the standings to the complete standings DataFrame
        # standings_complete = pd.concat([standings_complete, standings], ignore_index=True)

    return standings_complete


# Fetch and combine standings
standings_complete = fetch_and_combine_standings(auth_dir, game_code)

# Save the complete standings DataFrame to a CSV file
standings_complete.to_csv('fantasy_football_standings_2018_2023.csv', index=False)

# Output the DataFrame
print(standings_complete)

# Manually override league key for example code to work
# yahoo_query.league_key = f"{game_id}.l.{league_id}"

# Manually override player key for example code to work
# player_key = f"{game_id}.p.{player_id}"


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# RUN QUERIES # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# print(repr(yahoo_query.get_league_key(season)))
# print(repr(yahoo_query.get_current_user()))
# print(repr(yahoo_query.get_user_games()))
# print(repr(yahoo_query.get_user_leagues_by_game_key(game_key)))
# print(repr(yahoo_query.get_user_teams()))

# print(repr(yahoo_query.get_league_info()))
# print(repr(yahoo_query.get_league_metadata()))
# print(repr(yahoo_query.get_league_settings()))
# print(repr(yahoo_query.get_league_standings()))
# print(repr(yahoo_query.get_league_teams()))
# print(repr(yahoo_query.get_league_players(player_count_limit=10, player_count_start=0)))
# print(repr(yahoo_query.get_league_draft_results()))
# print(repr(yahoo_query.get_league_transactions()))
print(repr(yahoo_query.get_league_scoreboard_by_week(chosen_week)))
# print(repr(yahoo_query.get_league_matchups_by_week(chosen_week)))

# print(repr(yahoo_query.get_team_info(team_id)))
# print(repr(yahoo_query.get_team_metadata(team_id)))
# print(repr(yahoo_query.get_team_stats(team_id)))
# ERROR print(repr(yahoo_query.get_team_stats_by_week(team_id, chosen_week)))
# print(repr(yahoo_query.get_team_standings(team_id)))
# print(repr(yahoo_query.get_team_roster_by_week(team_id, chosen_week)))
# print(repr(yahoo_query.get_team_roster_player_info_by_week(team_id, chosen_week)))
# print(repr(yahoo_query.get_team_roster_player_info_by_date(team_id, chosen_date)))  # NHL/MLB/NBA
# print(repr(yahoo_query.get_team_roster_player_stats(team_id)))
# print(repr(yahoo_query.get_team_roster_player_stats_by_week(team_id, chosen_week)))
# print(repr(yahoo_query.get_team_draft_results(team_id)))
# print(repr(yahoo_query.get_team_matchups(team_id)))

# print(repr(yahoo_query.get_player_stats_for_season(player_key)))
# print(repr(yahoo_query.get_player_stats_for_season(player_key, limit_to_league_stats=False)))
# print(repr(yahoo_query.get_player_stats_by_week(player_key, chosen_week)))
# print(repr(yahoo_query.get_player_stats_by_week(player_key, chosen_week, limit_to_league_stats=False)))
# print(repr(yahoo_query.get_player_stats_by_date(player_key, chosen_date)))  # NHL/MLB/NBA
# print(repr(yahoo_query.get_player_stats_by_date(player_key, chosen_date, limit_to_league_stats=False)))  # NHL/MLB/NBA
# print(repr(yahoo_query.get_player_ownership(player_key)))
# print(repr(yahoo_query.get_player_percent_owned_by_week(player_key, chosen_week)))
# print(repr(yahoo_query.get_player_draft_analysis(player_key)))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CHECK FOR MISSING DATA FIELDS # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

logger = get_logger("yfpy.models", DEBUG)

# yahoo_query.get_all_yahoo_fantasy_game_keys()
# yahoo_query.get_game_key_by_season(season)
# yahoo_query.get_current_game_info()
# yahoo_query.get_current_game_metadata()
# yahoo_query.get_game_info_by_game_id(game_id)
# yahoo_query.get_game_metadata_by_game_id(game_id)
# yahoo_query.get_game_weeks_by_game_id(game_id)
# yahoo_query.get_game_stat_categories_by_game_id(game_id)
# yahoo_query.get_game_position_types_by_game_id(game_id)
# yahoo_query.get_game_roster_positions_by_game_id(game_id)
# yahoo_query.get_league_key(season)
# yahoo_query.get_current_user()
# yahoo_query.get_user_games()
# yahoo_query.get_user_leagues_by_game_key(game_key)
# yahoo_query.get_user_teams()
# yahoo_query.get_league_info()
# yahoo_query.get_league_metadata()
# yahoo_query.get_league_settings()
# yahoo_query.get_league_standings()
# yahoo_query.get_league_teams()
# yahoo_query.get_league_players(player_count_limit=10, player_count_start=0)
# yahoo_query.get_league_draft_results()
# yahoo_query.get_league_transactions()
# yahoo_query.get_league_scoreboard_by_week(chosen_week)
# yahoo_query.get_league_matchups_by_week(chosen_week)
# yahoo_query.get_team_info(team_id)
# yahoo_query.get_team_metadata(team_id)
# yahoo_query.get_team_stats(team_id)
# yahoo_query.get_team_stats_by_week(team_id, chosen_week)
# yahoo_query.get_team_standings(team_id)
# yahoo_query.get_team_roster_by_week(team_id, chosen_week)
# yahoo_query.get_team_roster_player_info_by_week(team_id, chosen_week)
# yahoo_query.get_team_roster_player_info_by_date(team_id, chosen_date)  # NHL/MLB/NBA
# yahoo_query.get_team_roster_player_stats(team_id)
# yahoo_query.get_team_roster_player_stats_by_week(team_id, chosen_week)
# yahoo_query.get_team_draft_results(team_id)
# yahoo_query.get_team_matchups(team_id)
# yahoo_query.get_player_stats_for_season(player_key))
# yahoo_query.get_player_stats_for_season(player_key, limit_to_league_stats=False))
# yahoo_query.get_player_stats_by_week(player_key, chosen_week)
# yahoo_query.get_player_stats_by_week(player_key, chosen_week, limit_to_league_stats=False)
# yahoo_query.get_player_stats_by_date(player_key, chosen_date,)  # NHL/MLB/NBA
# yahoo_query.get_player_stats_by_date(player_key, chosen_date, limit_to_league_stats=False)  # NHL/MLB/NBA
# yahoo_query.get_player_ownership(player_key)
# yahoo_query.get_player_percent_owned_by_week(player_key, chosen_week)
# yahoo_query.get_player_draft_analysis(player_key)
