from app.models.sport_models import Sport
from ..models.soccer_models import SoccerStat
from .sport_accessor import SportAccessor
from ..mappers.soccer_mapper import map_rows_to_teams
from ..mappers.sport_mapper import map_row_to_stat
from ..db_utils import execute_sql_statement
from enum import Enum

from ..mappers.soccer_mapper import *
from ..models.soccer_models import *
from ..db_utils import DB,execute_bulk_insert,fetchone_sql_statement



class Stat(Enum):
    GOALS = 1
    ASSISTS = 2

class SoccerAccessor(SportAccessor):

    def __init__(self):
        super().__init__(Sport.SOCCER)
    
    def get_teams_data(self,season_id: int):
        teams_query = "SELECT team_id, season_id, team_name, team_captain, wins, losses, draws, goals_for, goals_against, points FROM Teams WHERE season_id=?"
        teams_records = execute_sql_statement(self.SPORT,teams_query,(season_id,))
        teams = map_rows_to_teams(teams_records) 
        return teams

    def get_game_stats_data(self,game_id: int):
        game_stats_query= "SELECT g_id,t_id,team_name,goals,assists FROM game_totals WHERE g_id = ?"
        games_records = execute_sql_statement(self.SPORT,game_stats_query,(game_id,))
        games = map_row_to_stat(games_records)
        return games

    def get_player_stats_data(self,stat: SoccerStat,season_id: int):
        stat_query = ""
        if stat == SoccerStat.GOALS:
            stat_query = "SELECT p_id,name,games_played,goals FROM player_totals WHERE season_id=?"
        elif stat == SoccerStat.ASSISTS:
            stat_query = "SELECT p_id,name,games_played,assists FROM player_totals WHERE season_id=?"

        stat_records = execute_sql_statement(self.SPORT,stat_query,(season_id,))  
        player_stats = map_row_to_stat(stat_records)
        
        return player_stats 



#--------------
# Backend Accesssor  
#--------------
def insert_soccer_stats(stats: list[SoccerStat]):
    gameID = stats[0].game_id

    # Only insert game stats if they dont already exsist 
    isGameAdded = check_for_game_stats(gameID)

    if isGameAdded: raise ValueError('this game has been previously populated'.format(gameID))

    stat_values = [(stat.game_id,stat.player_id,stat.goals,stat.assists,) for stat in stats]
    query_insert = """
    INSERT INTO statistics (game_id, player_id, goals, assists)
    VALUES (?, ?, ?, ?);
    """
    execute_bulk_insert(DB.SOCCER,query_insert,stat_values)

def check_for_game_stats(gameID: int)-> bool: 
    check_games_query = """
    SELECT game_id 
    FROM statistics
    WHERE game_id = ? LIMIT 1;
    """
    record = fetchone_sql_statement(DB.SOCCER,check_games_query,(gameID,))
    if not record: return False 
    return True