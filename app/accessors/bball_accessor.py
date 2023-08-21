from .sport_accessor import SportAccessor

from app.models.sport_models import Sport
from ..models.bball_models import BballStat
from ..mappers.sport_mapper import map_row_to_stat,map_row_to_games
from ..mappers.bball_mapper import map_row_to_team 
from ..db_utils import execute_sql_statement


class BasketballAccessor(SportAccessor):

    def __init__(self):
        super().__init__(Sport.BASKETBALL)
    
    def get_teams_data(self,season_id: int):
        teams_query = "SELECT team_id,team_name,wins,losses,PF,PA,rebounds_tot FROM Teams WHERE season_id=?"
        teams_records = execute_sql_statement(self.SPORT,teams_query,(season_id,))
        teams = map_row_to_team(teams_records) 
        return teams

    def get_game_stats_data(self,game_id: int):
        game_stats_query= "SELECT g_id,t_id,team_name,total_pts,total_reb,fls FROM game_totals WHERE g_id = ?"
        games_records = execute_sql_statement(self.SPORT,game_stats_query,(game_id,))
        games = map_row_to_games(games_records)
        return games

    def get_player_stats_data(self,stat: BballStat,season_id: int):
        stat_query = ""
        if stat == BballStat.POINTS:
            stat_query = "SELECT p_id,name,games_played,points FROM player_totals WHERE season_id=?"
        elif stat == BballStat.REBOUNDS:
            stat_query = "SELECT p_id,name,games_played,rebounds FROM player_totals WHERE season_id=?"

        stat_records = execute_sql_statement(self.SPORT,stat_query,(season_id,))  
        player_stats = map_row_to_stat(stat_records)
        return player_stats 
    
