from app.models.sport_models import Sport
from ..models.soccer_models import SoccerStat
from .sport_accessor import SportAccessor
from ..mappers.sport_mapper import map_row_to_stat
from ..mappers.soccer_mapper import map_row_to_soccer_game_stats
from ..db_utils import execute_sql_statement
from enum import Enum

from ..mappers.soccer_mapper import *
from ..models.soccer_models import *
from ..db_utils import DB,execute_bulk_query,fetchone_sql_statement



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
        games = map_row_to_soccer_game_stats(games_records)
        return games

    def get_player_stats_data(self,stat: SoccerStat,season_id: int):
        stat_query = ""
        if stat == SoccerStat.GOALS:
            stat_query = "SELECT p_id,player_name,games_played,goals FROM player_totals WHERE season_id=?"
        elif stat == SoccerStat.ASSISTS:
            stat_query = "SELECT p_id,player_name,games_played,assists FROM player_totals WHERE season_id=?"

        stat_records = execute_sql_statement(self.SPORT,stat_query,(season_id,))  
        player_stats = map_row_to_stat(stat_records)
        
        return player_stats 

    def get_game_player_stats_data(self, game_id: int):
        game_stats_query= "SELECT game_id, team_id, team_name, player_id, stat_id, player_name, dnp, goals, assists FROM game_statistics WHERE game_id = ?"
        games_records = execute_sql_statement(self.SPORT, game_stats_query,(game_id,))
        games = map_row_to_player_game_stats(games_records)
        return games

    def insert_soccer_stats(self, stats: list[SoccerStatUpsert]):
        stat_values = [(stat.game_id,stat.player_id,stat.dnp,stat.goals,stat.assists) for stat in stats]
        query_insert = """
        INSERT INTO statistics (game_id, player_id, dnp, goals, assists)
        VALUES (?, ?, ?, ?, ?);
        """
        execute_bulk_query(self.SPORT,query_insert,stat_values)

    def update_soccer_stats(self, stats: list[SoccerStatUpsert]):
        stat_values = [(stat.dnp, stat.goals, stat.assists, stat.stat_id) for stat in stats]
        query_update = """
            UPDATE statistics 
            SET dnp = ?,
                goals = ?,
                assists = ?
            WHERE
                stat_id = ? 
            ORDER BY
                stat_id
            LIMIT 1;       
        """
        execute_bulk_query(self.SPORT, query_update, stat_values)