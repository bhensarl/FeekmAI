from yfpy.logger import get_logger
from logging import DEBUG


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# RUN QUERIES # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# print(repr(yahoo_query.get_all_yahoo_fantasy_game_keys()))
# print(repr(yahoo_query.get_game_key_by_season(season)))
# print(repr(yahoo_query.get_current_game_info()))
# print(repr(yahoo_query.get_current_game_metadata()))
# print(repr(yahoo_query.get_game_info_by_game_id(game_id)))
# print(repr(yahoo_query.get_game_metadata_by_game_id(game_id)))
# print(repr(yahoo_query.get_game_weeks_by_game_id(game_id)))
# print(repr(yahoo_query.get_game_stat_categories_by_game_id(game_id)))
# print(repr(yahoo_query.get_game_position_types_by_game_id(game_id)))
# print(repr(yahoo_query.get_game_roster_positions_by_game_id(game_id)))
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
# print(repr(yahoo_query.get_league_scoreboard_by_week(chosen_week)))
# print(repr(yahoo_query.get_league_matchups_by_week(chosen_week)))

# print(repr(yahoo_query.get_team_info(team_id)))
# print(repr(yahoo_query.get_team_metadata(team_id)))
# print(repr(yahoo_query.get_team_stats(team_id)))
# print(repr(yahoo_query.get_team_stats_by_week(team_id, chosen_week)))
# print(repr(yahoo_query.get_team_standings(team_id)))
# print(repr(yahoo_query.get_team_roster_by_week(team_id, chosen_week)))
# print(repr(yahoo_query.get_team_roster_player_info_by_week(team_id, chosen_week)))
# # print(repr(yahoo_query.get_team_roster_player_info_by_date(team_id, chosen_date)))  # NHL/MLB/NBA
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
