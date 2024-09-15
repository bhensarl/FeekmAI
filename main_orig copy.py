import pandas as pd
import os
from yahoo_fantasy_sports_query import YahooFantasySportsQuery

# from variable setup import located at top of file.  Adjust that if you want to pull additional variables.
season = get_season()
game_code = get_game_code()
game_id = get_game_id()
game_key = get_game_key()
league_id = get_league_id()
team_name = get_team_name()
get_player_id = get_player_id()

# Dictionary linking years to their respective league IDs
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
        for week in range(1, 19):  # Loop through weeks 1 to 18
            print(f"Processing year: {year}, Week: {week}")  # Debug print to show the current year and week being processed
            print(f"Game ID: {ids['game_id']}, League ID: {ids['league_id']}")
            
            league_id = ids["league_id"]
            game_id = ids["game_id"]

            # Print the game_id and league_id to debug
            print(f"Debug: Year: {year}, Game ID: {game_id}, League ID: {league_id}, Week: {week}")

            # Initialize the YahooFantasySportsQuery object for the current year and week
            yahoo_query = YahooFantasySportsQuery(
                auth_dir,
                league_id,
                game_id,
                week,
                offline=False,
                all_output_as_json_str=False,
                consumer_key=os.environ["YFPY_CONSUMER_KEY"],
                consumer_secret=os.environ["YFPY_CONSUMER_SECRET"]
            )

            # Manually override league key for example code to work
            yahoo_query.league_key = f"{game_id}.l.{league_id}"

            # Fetch the standings for the current year and week
            standings = yahoo_query.get_league_standings()
            print(standings)
            
            # Add a column to the standings DataFrame to indicate the year and week
            standings['Year'] = year
            standings['Week'] = week

            # Append the standings to the complete standings DataFrame
            standings_complete = pd.concat([standings_complete, standings], ignore_index=True)

    return standings_complete

# Fetch and combine standings
standings_complete = fetch_and_combine_standings(auth_dir, game_code)

# Save the complete standings DataFrame to a CSV file
standings_complete.to_csv('fantasy_football_standings_2018_2023.csv', index=False)

# Output the DataFrame
print(standings_complete)
