#!/usr/bin/env python
# coding: utf-8

# Test.  Is this working?  GIT!

# In[1]:


# v1.7 change log
# -Fixed long lines
# -Refactored load_weekly_data function
# -Commented out the update_cumulative_data function
# BACKLOG
# -Doints calculator
# -Koints calculator
# -Boints calculator


# In[ ]:


# !/usr/bin/env python
# coding: utf-8

"""
This script processes and analyzes weekly sports data (e.g., football scores) from JSON files.
It generates various reports, including team scoreboards, division scoreboards, and identifies
the "Bad Beats" and "Overachievers" of each week.
"""


# In[2]:


import json
import pandas as pd
import numpy as np
import datetime

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Pandas for data manipulation
# json for parsing JSON data


# In[3]:


def load_weekly_data(week_number):
    """
    Load data from a JSON file for a given week.

    :param week_number: Week number as a string (e.g., '1' for week1.json)
    :return: Data loaded from the JSON file
    """
    file_path = f'scores/week{week_number}.json'

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        data = {}

    # Ensure the data is in the expected dictionary format
    if isinstance(data, list):
        # If the data is a list, try to get the first element assuming it might be the correct dict
        data = data[0] if data else {}

    return data


# In[4]:


def extract_data(weekly_data, cumulative_data, all_data):
    """
    Extract relevant data from the weekly JSON data and convert it to a DataFrame.

    :param weekly_data: Data loaded from the JSON file
    :param cumulative_data: Cumulative data for win/loss record
    :param all_data: DataFrame with all previously extracted data
    :return: DataFrame with extracted data
    """
    extracted_data = []
    if isinstance(weekly_data, dict) and 'matchups' in weekly_data:
        for matchup in weekly_data['matchups']:
            teams = matchup['matchup']['teams']
            if len(teams) != 2:  # Ensure there are exactly two teams in a matchup
                continue

            n_vs_s = 'Y' if teams[0]['team']['division_id'] != teams[1]['team']['division_id'] else 'N'

            points_against = {teams[0]['team']['team_id']: float(teams[1]['team']['team_points']['total']),
                              teams[1]['team']['team_id']: float(teams[0]['team']['team_points']['total'])
                              }

            for team in teams:
                team_data = team['team']
                team_id = team_data['team_id']
                win = team_data['team_key'] == matchup['matchup'].get('winner_team_key')
                loss = not win

                if team_id not in cumulative_data:
                    cumulative_data[team_id] = {'wins': 0, 'losses': 0}
                cumulative_data[team_id]['wins'] += win
                cumulative_data[team_id]['losses'] += loss

                extracted_data.append({
                    'week': weekly_data['week'],
                    'team_name': team_data['name'],
                    'projected_points': float(team_data['team_projected_points']['total']),
                    'points': float(team_data['team_points']['total']),
                    'win_or_loss': 'Win' if win else 'Loss',
                    'n_vs_s': n_vs_s,
                    'total_wins': cumulative_data[team_id]['wins'],
                    'total_losses': cumulative_data[team_id]['losses'],
                    'division_id': team_data['division_id'],
                    'points_against': points_against[team_data['team_id']],
                    'inter_division_win': (win and n_vs_s == 'Y')
                })

    else:
        if isinstance(weekly_data, dict):
            print(f"Data format error in week {weekly_data.get('week', 'unknown')}")
        else:
            print("Data format error: weekly_data is not a dictionary")

    weekly_df = pd.DataFrame(extracted_data)

    # Calculate cumulative points, Points For/Against Ratio, and running averages
    for team in weekly_df['team_name'].unique():
        team_df = weekly_df[weekly_df['team_name'] == team]
        team_points = team_df['points']
        team_points_against = team_df['points_against']

        if not all_data.empty:
            previous_points = all_data[all_data['team_name'] == team]['points'].sum()
            previous_points_against = all_data[all_data['team_name'] == team]['points_against'].sum()
            previous_games = all_data[all_data['team_name'] == team].shape[0]
        else:
            previous_points = 0
            previous_points_against = 0
            previous_games = 0

        cumulative_points = previous_points + team_points.cumsum()
        cumulative_points_against = previous_points_against + team_points_against.cumsum()
        games_played = previous_games + team_df.shape[0]

        weekly_df.loc[weekly_df['team_name'] == team, 'cumulative_points'] = cumulative_points
        # Calculate and assign Points For/Against Ratio
        ratio = cumulative_points / cumulative_points_against.replace(0, 1)
        weekly_df.loc[weekly_df['team_name'] == team, 'points_for_against_ratio'] = ratio
        # Calculate and assign running averages
        weekly_df.loc[weekly_df['team_name'] == team, 'average_points_for'] = cumulative_points / games_played
        weekly_df.loc[weekly_df['team_name'] == team, 'average_points_against'] = cumulative_points_against / games_played

    return weekly_df


# In[5]:


# def update_cumulative_data(df, cumulative_df):
#     """
#     Update cumulative data for each team and division.
#
#     :param df: DataFrame with weekly data
#     :param cumulative_df: DataFrame with cumulative data
#     :return: Updated cumulative DataFrame
#     """
#     # Update team points and win/loss records
#     for index, row in df.iterrows():
#         team_id = row['team_id']
#         team_points = row['team_points']
#         win = row['win_probability'] > 0.5
#
#         if team_id not in cumulative_df.index:
#             cumulative_df.loc[team_id] = {'total_points': 0, 'wins': 0, 'losses': 0, 'division_points': 0}
#
#         cumulative_df.at[team_id, 'total_points'] += team_points
#         cumulative_df.at[team_id, 'wins'] += win
#         cumulative_df.at[team_id, 'losses'] += not win
#
#     # Update division points
#     division_points = df.groupby('division_id')['team_points'].sum()
#     for division_id, points in division_points.items():
#         cumulative_df.loc[cumulative_df['division_id'] == division_id, 'division_points'] += points
#
#     return cumulative_df


# In[6]:


def create_scoreboard(df):
    """
    Create a weekly scoreboard DataFrame.

    :param df: DataFrame with detailed weekly data
    :return: DataFrame representing the weekly scoreboard
    """
    # Map division IDs to names
    division_names = {'2': 'North', '1': 'South'}

    # Aggregate data
    agg_data = df.groupby(['division_id', 'team_name']).agg({
        'total_wins': 'max',
        'total_losses': 'max',
        'points': 'sum',
        'points_against': 'sum',
        'inter_division_win': 'sum'
    }).reset_index()

    # Rename columns and map division names
    agg_data.rename(columns={
        'division_id': 'Division',
        'team_name': 'Team Name',
        'total_wins': 'Win',
        'total_losses': 'Loss',
        'points': 'Total Points',
        'points_against': 'Total Points Against',
        'inter_division_win': 'Inter-Division Wins'
    }, inplace=True)

    agg_data['Division'] = agg_data['Division'].map(division_names)

    # Convert columns to numeric types
    agg_data['Total Points'] = pd.to_numeric(agg_data['Total Points'], errors='coerce')
    agg_data['Total Points Against'] = pd.to_numeric(agg_data['Total Points Against'], errors='coerce')

    # Calculate total games played (total wins + total losses)
    agg_data['Total Games'] = agg_data['Win'] + agg_data['Loss']

    # Calculate Avg Pts For and Avg Pts Against
    agg_data['Avg Pts For'] = (agg_data['Total Points'] / agg_data['Total Games']).round(2)
    agg_data['Avg Pts Against'] = (agg_data['Total Points Against'] / agg_data['Total Games']).round(2)

    # Sort by Total Wins and Total Points, then calculate Rank across all teams
    sorted_agg_data = agg_data.sort_values(['Win', 'Total Points'], ascending=[False, False])
    sorted_agg_data['Rank'] = range(1, len(sorted_agg_data) + 1)

    # Calculate Pts For/Against Ratio
    # Replace zero values in 'Total Points Against' with NaN
    points_against = sorted_agg_data['Total Points Against'].replace(0, np.nan)

    # Calculate the ratio and round to 3 decimal places
    sorted_agg_data['Pts For/Against Ratio'] = (sorted_agg_data['Total Points'] / points_against).round(3)

    # Order columns as specified
    scoreboard = sorted_agg_data[[
        'Division', 'Team Name', 'Rank', 'Win', 'Loss', 'Total Points',
        'Total Points Against', 'Inter-Division Wins', 'Avg Pts For',
        'Avg Pts Against', 'Pts For/Against Ratio'
    ]]

    return scoreboard


# In[7]:


def identify_bad_beats(df):
    # Initialize an empty DataFrame for bad_beats
    bad_beats = pd.DataFrame(columns=['Week', 'Bad Beats Team of the Week'])

    # Check if there are any losses
    if df['win_or_loss'].eq('Loss').any():
        # Calculate the margin of loss
        df['loss_margin'] = df['points_against'] - df['points']

        # Filter for losses
        losses = df[df['win_or_loss'] == 'Loss']

        # Identify the team with the largest loss margin for each week
        bad_beats = losses.groupby('week').apply(
            lambda x: x.loc[x['loss_margin'].idxmax()]['team_name']
        ).reset_index(name='Bad Beats Team of the Week')

    # Ensure 'Week' is in the correct format
    bad_beats.rename(columns={'week': 'Week'}, inplace=True)

    return bad_beats


# In[8]:


def calculate_division_scores(detailed_df):
    """
    Calculate and return a DataFrame with weekly scores for each division,
    including additional details, cumulative points, Bad Beats, and Overachievers.

    :param detailed_df: Original detailed DataFrame with all weekly data
    :return: DataFrame with weekly division scores and other details
    """
    # Convert 'week' to integer for proper sorting and calculations
    detailed_df['week'] = detailed_df['week'].astype(int)

    # Map division IDs to names
    division_names = {'1': 'South', '2': 'North'}  # Swapped mapping

    # Aggregate weekly points and inter-division wins per division
    weekly_aggregates = detailed_df.groupby(['week', 'division_id']).agg({
        'points': 'sum',  # Sum of game points by division
        'inter_division_win': 'sum'  # Count of inter-division wins
    }).reset_index()

    # Map division names
    weekly_aggregates['division_id'] = weekly_aggregates['division_id'].map(division_names)
    weekly_aggregates.rename(columns={'division_id': 'Division', 'week': 'Week'}, inplace=True)

    # Pivot to create weekly scoreboards for each division
    division_scoreboard = weekly_aggregates.pivot(
        index='Week', columns='Division', values=['points', 'inter_division_win']
    ).fillna(0)

    # Flatten MultiIndex in columns after pivot
    division_scoreboard.columns = [
        ' '.join(col).strip() for col in division_scoreboard.columns.values
    ]
    division_scoreboard.reset_index(inplace=True)

    # Convert 'inter_division_win' columns to integers
    division_scoreboard['inter_division_win North'] = division_scoreboard['inter_division_win North'].astype(int)
    division_scoreboard['inter_division_win South'] = division_scoreboard['inter_division_win South'].astype(int)

    # Adjust the calculation of total points
    for division in ['North', 'South']:
        # Initialize total points column
        division_scoreboard[f'{division} Div Total Pts'] = 0

        # Iterate over each week
        for week in division_scoreboard['Week']:
            # Calculate points for current week
            current_week_points = division_scoreboard.loc[division_scoreboard['Week'] == week, f'points {division}'].iloc[0]
            inter_division_wins = division_scoreboard.loc[division_scoreboard['Week'] == week, f'inter_division_win {division}'].iloc[0]
            additional_points = 100 * inter_division_wins

            if week > 1:
                # Add to previous week's total points
                previous_total = division_scoreboard.loc[division_scoreboard['Week'] == week - 1, f'{division} Div Total Pts'].iloc[0]
                division_scoreboard.loc[division_scoreboard['Week'] == week, f'{division} Div Total Pts'] = previous_total + current_week_points + additional_points
            else:
                # For the first week, the total is just the current week's points
                division_scoreboard.loc[division_scoreboard['Week'] == week, f'{division} Div Total Pts'] = current_week_points + additional_points

    # Identify the highest scoring team for each week (BMOC)
    highest_scoring_team = detailed_df.groupby('week')['points'].idxmax()
    bmoc = detailed_df.loc[highest_scoring_team, ['week', 'team_name']].reset_index(drop=True)
    bmoc.rename(columns={'week': 'Week', 'team_name': 'BMOC'}, inplace=True)

    # Ensure 'Week' column is integer in all DataFrames
    division_scoreboard['Week'] = division_scoreboard['Week'].astype(int)
    bmoc['Week'] = bmoc['Week'].astype(int)

    # Merge BMOC with division_scoreboard
    division_scoreboard = pd.merge(division_scoreboard, bmoc, on='Week', how='left')

    # Functions to identify Overachievers
    def identify_overachievers(df):
        df['points_above_projected'] = df['points'] - df['projected_points']
        overachievers = df.groupby('week').apply(
            lambda x: x.loc[x['points_above_projected'].idxmax()]['team_name']
        ).reset_index(name='Overachiever of the Week')
        overachievers.rename(columns={'week': 'Week'}, inplace=True)
        return overachievers

    # Get Bad Beats and Overachievers
    bad_beats = identify_bad_beats(detailed_df)
    overachievers = identify_overachievers(detailed_df)

    # Ensure 'Week' column is integer in all DataFrames
    division_scoreboard['Week'] = division_scoreboard['Week'].astype(int)
    bad_beats['Week'] = bad_beats['Week'].astype(int)
    overachievers['Week'] = overachievers['Week'].astype(int)

    # Merge Bad Beats and Overachievers with division_scoreboard
    division_scoreboard = pd.merge(division_scoreboard, bad_beats, on='Week', how='left')
    division_scoreboard = pd.merge(division_scoreboard, overachievers, on='Week', how='left')

    return division_scoreboard


# In[9]:


# Generate all_data_df to feed data to functions

# Initialize dictionary for cumulative win/loss data
cumulative_data = {}

# Initialize DataFrame for all extracted data
all_data_df = pd.DataFrame()

# Set week number
week_no = 17

# Process each week
for week in range(1, week_no + 1):  # Assuming 17 weeks in the season
    weekly_data = load_weekly_data(str(week))
    weekly_df = extract_data(weekly_data, cumulative_data, all_data_df)
    all_data_df = pd.concat([all_data_df, weekly_df], ignore_index=True)

# Display the final DataFrame
all_data_df


# In[ ]:

# In[10]:


# TEAM WEEKLY SCOREBOARD

weekly_scoreboard = create_scoreboard(all_data_df)
weekly_scoreboard


# In[11]:


# DIVISION WEEKLY SCOREBOARD

division_detailed_scoreboard = calculate_division_scores(all_data_df)
division_detailed_scoreboard


# In[12]:

# Get current date and time
current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# File names with date and time prefix
all_data_filename = f'data/{current_datetime}_feek_all_data.csv'
division_scoreboard_filename = f'data/{current_datetime}_feek_division_scoreboard.csv'
weekly_scoreboard_filename = f'data/{current_datetime}_feek_weekly_scoreboard.csv'

# Saving the detailed weekly data for teams
all_data_df.to_csv(
    all_data_filename, index=False
)

# Saving the weekly division scoreboard with cumulative points
division_detailed_scoreboard.to_csv(
    division_scoreboard_filename, index=False
)

# Saving the weekly scoreboard
weekly_scoreboard.to_csv(
    weekly_scoreboard_filename, index=False
)
