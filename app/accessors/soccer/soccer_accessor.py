from .soccer_mapper import *
from .soccer_models import *
from ..db_utils import DB,execute_sql_statement,fetchone_sql_statement,commit_sql_statement

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


