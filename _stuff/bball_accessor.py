from .sport_accessor import SportAccessor

from app.models.sport_models import Sport
from ..models.bball_models import BballStat, BballStatUpsert, BballTeamStats
from ..mappers.sport_mapper import map_row_to_stat,map_row_to_games
from ..mappers.bball_mapper import map_row_to_team, map_row_to_game_stats, map_row_to_player_game_stats
from ..db_utils import execute_sql_statement, execute_bulk_query, commit_sql_statement


class BasketballAccessor(SportAccessor):

    def __init__(self):
        super().__init__(Sport.BASKETBALL)
    
    def get_teams_data(self,season_id: int):
        teams_query = "SELECT team_id, season_id, team_name, team_captain, wins,losses,PF,PA,rebounds_tot FROM Teams WHERE season_id=?"
        teams_records = execute_sql_statement(self.SPORT,teams_query,(season_id,))
        teams = map_row_to_team(teams_records) 
        return teams

    def get_game_stats_data(self,game_id: int):
        game_stats_query= "SELECT g_id,t_id,team_name,total_pts,total_reb,fls FROM game_totals WHERE g_id = ?"
        games_records = execute_sql_statement(self.SPORT,game_stats_query,(game_id,))
        games = map_row_to_game_stats(games_records)
        return games

    def get_team_game_stats_data(self, gameIDs: list[int]):
        placeholders = ','.join(['?'] * len(gameIDs))
        game_stats_query= f"SELECT g_id,t_id,team_name,total_pts,total_reb,fls FROM game_totals WHERE g_id IN ({placeholders})"
        games_records = execute_sql_statement(self.SPORT,game_stats_query,gameIDs)
        games = map_row_to_game_stats(games_records)
        return games

    def update_team_season_stats(self, team_id, sts: BballTeamStats):
        stat_values = [sts.wins, sts.losses, sts.points_for, sts.points_against, sts.rebounds, sts.fouls, team_id]
        query_update = """
            UPDATE teams 
            SET wins = ?,
                losses = ?,
                PF = ?,
                PA = ?,
                rebounds_tot = ?,
                fouls_tot = ?
            WHERE
                team_id = ? 
            ORDER BY
                team_id
            LIMIT 1;       
        """
        commit_sql_statement(self.SPORT, query_update, stat_values)


    def get_player_stats_data(self,stat: BballStat,season_id: int):
        stat_query = ""
        if stat == BballStat.POINTS:
            stat_query = "SELECT p_id,name,games_played,points FROM player_totals WHERE season_id=?"
        elif stat == BballStat.REBOUNDS:
            stat_query = "SELECT p_id,name,games_played,rebounds FROM player_totals WHERE season_id=?"


        stat_records = execute_sql_statement(self.SPORT,stat_query,(season_id,))  
        player_stats = map_row_to_stat(stat_records)
        return player_stats 
    

    def get_game_player_stats_data(self, game_id: int):
        game_stats_query= "SELECT game_id, team_id, team_name, player_id, stat_id, player_name, dnp, points, rebounds, fouls FROM game_statistics WHERE game_id = ?"
        games_records = execute_sql_statement(self.SPORT,game_stats_query,(game_id,))
        games = map_row_to_player_game_stats(games_records)
        return games


    def insert_bball_stats(self, stats: list[BballStatUpsert]):
        stat_values = [(stat.game_id,stat.player_id,stat.dnp,stat.points,stat.rebounds,stat.fouls) for stat in stats]
        query_insert = """
        INSERT INTO statistics (game_id, player_id, dnp, points, rebounds, fouls)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        execute_bulk_query(self.SPORT,query_insert,stat_values)


    def update_bball_stats(self, stats: list[BballStatUpsert]):
        stat_values = [(stat.dnp, stat.points, stat.rebounds,stat.fouls, stat.stat_id) for stat in stats]
        query_update = """
            UPDATE statistics 
            SET dnp = ?,
                points = ?,
                rebounds = ?,
                fouls = ?
            WHERE
                stat_id = ? 
            ORDER BY
                stat_id
            LIMIT 1;       
        """
        execute_bulk_query(self.SPORT, query_update, stat_values)
