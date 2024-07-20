# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# VARIABLE SETUP  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# set desired season year
def get_season():
    season = 2023
    return season


season = get_season()


# set desired week
def get_chosen_week():
    chosen_week = 1
    return chosen_week


chosen_week = get_chosen_week()


# set desired date
def get_chosen_date():
    # HOCKEY
    # chosen_date = "2013-04-15"  # NHL - 2013 (for 2012 season)
    # chosen_date = "2021-10-25"  # NHL - 2021
    chosen_date = "2021-10-25"  # NHL - 2021

    # BASEBALL
    # chosen_date = "2021-04-01"  # MLB - 2021
    # chosen_date = "2022-04-10"  # MLB - 2022

    return chosen_date


chosen_date = get_chosen_date()


# set desired Yahoo Fantasy Sports game code
def get_game_code():
    # FOOTBALL
    game_code = "nfl"  # NFL

    # HOCKEY
    # game_code = "nhl"  # NHL

    # BASEBALL
    # game_code = "mlb"  # MLB

    return game_code


game_code = get_game_code()


# set desired Yahoo Fantasy Sports game ID (see the get_all_yahoo_fantasy_game_keys query to retrieve values)
def get_game_id():
    # FOOTBALL
    # game_id = 331  # NFL - 2014
    # game_id = 348  # NFL - 2015 (divisions)
    # game_id = 359  # NFL - 2016
    # game_id = 371  # NFL - 2017
    # game_id = 380  # NFL - 2018
    # game_id = 390  # NFL - 2019
    # game_id = 399  # NFL - 2020
    # game_id = 406  # NFL - 2021
    # game_id = 414  # NFL - 2022 (divisions)
    game_id = 423  # NFL - 2023

    # HOCKEY
    # game_id = 303  # NHL - 2012
    # game_id = 411  # NHL - 2021
    # game_id = 427  # NHL - 2023

    # BASEBALL
    # game_id = 404  # MLB - 2021
    # game_id = 412  # MLB - 2022

    return game_id


game_id = get_game_id()


# set desired Yahoo Fantasy Sports game key (see the get_all_yahoo_fantasy_game_keys query to retrieve values)
def get_game_key():
    # FOOTBALL
    # game_key = "331"  # NFL - 2014
    # game_key = "348"  # NFL - 2015 (divisions)
    # game_key = "359"  # NFL - 2016
    # game_key = "371"  # NFL - 2017
    # game_key = "380"  # NFL - 2018
    # game_key = "390"  # NFL - 2019
    # game_key = "399"  # NFL - 2020
    # game_key = "406"  # NFL - 2021
    # game_key = "414"  # NFL - 2022 (divisions)
    game_key = "423"  # NFL - 2023

    # HOCKEY
    # game_key = "303"  # NHL - 2012
    # game_key = "411"  # NHL - 2021
    # game_key = "427"  # NHL - 2023

    # BASEBALL
    # game_key = "404"  # MLB - 2021
    # game_key = "412"  # MLB - 2022

    return game_key


game_key = get_game_key()


# set desired league ID (see README.md for finding value)
def get_league_id():
    # FOOTBALL
    # league_id = "67583"  # NFL - 2018 FeekmaFeek https://football.fantasysports.yahoo.com/2018/f1/67583
    # league_id = "43068"  # NFL - 2019 FeekmaFeek https://football.fantasysports.yahoo.com/2019/f1/43068
    # league_id = "643103"  # NFL - 2020 FeekmaFeek https://football.fantasysports.yahoo.com/2020/f1/643103
    # league_id = "333658"  # NFL - 2021 FeekmaFeek https://football.fantasysports.yahoo.com/2021/f1/333658
    # league_id = "74941"  # NFL - 2022 FeekmaFeek https://football.fantasysports.yahoo.com/2022/f1/74941
    league_id = "219013"  # NFL - 2023 FeekmaFeek https://football.fantasysports.yahoo.com/2023/f1/219013

    return league_id


league_id = get_league_id()


# set desired team ID within desired league
def get_team_id():
    # FOOTBALL
    team_id = 1  # NFL

    # HOCKEY
    # team_id = 2  # NHL (2012)

    return team_id


team_id = get_team_id()


# set desired team name within desired league
def get_team_name():
    # FOOTBALL
    team_name = "Legion"  # NFL

    # HOCKEY
    # team_name = "The Bateleurs"  # NHL (2012)

    return team_name


team_name = get_team_name()


# set desired team ID within desired league
def get_player_id():
    # FOOTBALL
    player_id = 30123  # NFL: Patrick Mahomes - 2020/2021/2023

    return player_id


player_id = get_player_id()


# set the maximum number players you wish the get_league_players query to retrieve
def get_league_player_limit():
    league_player_limit = 101

    return league_player_limit


league_player_limit = get_league_player_limit()
