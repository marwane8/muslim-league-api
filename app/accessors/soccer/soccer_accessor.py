from .soccer_mapper import *
from .soccer_models import *
from ..db_utils import DB,execute_sql_statement,fetchone_sql_statement,commit_sql_statement

#--------------
# Seasons  
#--------------
def get_seasons_data() -> list[Season]:
    teams_query = "SELECT season_id, season_name, year FROM seasons"
    teams_records = execute_sql_statement(DB.SOCCER,teams_query)
    teams = map_rows_to_seasons(teams_records) 
    return teams


#--------------
# Teams  
#--------------
def get_teams_data(season_id: int) -> list[Team]:
    teams_query = "SELECT team_id, season_id, team_name, team_captain, wins, losses, draws, goals_for, goals_against, points FROM Teams WHERE season_id=?"
    teams_records = execute_sql_statement(DB.SOCCER,teams_query,(season_id,))
    teams = map_rows_to_teams(teams_records) 
    return teams

#--------------
# Player  
#--------------
def get_players_data(team_id: int) -> list[Player]:
    players_query = "SELECT id,team_id,team_name,player_name,player_number,player_pos FROM roster WHERE team_id=?"
    players_records = execute_sql_statement(DB.SOCCER,players_query,(team_id,))
    players = map_rows_to_players(players_records) 
    return players 


def get_player_totals_data(season_id: int=None) -> list[PlayerTotals]:
    #TODO: Implement Season Filter in DB
    player_totals_query = "SELECT p_id, player_name, games_played, goals, assists FROM player_totals"
    player_totals_records = execute_sql_statement(DB.SOCCER,player_totals_query)
    player_totals = map_rows_to_player_totals(player_totals_records) 
    return player_totals

#--------------
# Games  
#--------------
def get_game_dates(season_id: int) -> list[int]:
    game_day_query = "SELECT date FROM Games GROUP BY date"
    game_days_records= execute_sql_statement(DB.SOCCER,game_day_query)
    dates = [record[0] for record in game_days_records] 
    return dates

def get_games_of_date(date: int) -> list[Game]:
    game_query= "SELECT game_id,team1_id,team1,team2_id,team2,date,start_time,court,playoff FROM schedule WHERE date = ?"
    games_records = execute_sql_statement(DB.SOCCER,game_query,(date,))
    games = map_rows_to_games(games_records)
    return games

def get_game_stats_data(game_id: int) -> list[GameStats]:
    game_stats_query= "SELECT g_id,t_id,team_name,goals,assists FROM game_totals WHERE g_id = ?"
    games_records = execute_sql_statement(DB.SOCCER,game_stats_query,(game_id,))
    games = map_rows_to_stats(games_records)
    return games

