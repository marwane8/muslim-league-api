import sqlite3
from abc import ABC, abstractmethod

from ..models.sport_models import Sport, Stat
from ..mappers.sport_mapper import *
from ..db_utils import DB_STR, execute_sql_statement, execute_bulk_query, insert_many_to_many_query

class SportAccessor(ABC):
    def __init__(self,sport: Sport):
        self.SPORT = sport
    
    def get_seasons_data(self):
        teams_query = "SELECT season_id, season_name, year FROM seasons"
        teams_records = execute_sql_statement(self.SPORT,teams_query)
        teams = map_rows_to_seasons(teams_records) 
        return teams 

    def get_players_data(self,team_id: int):
        players_query = "SELECT id,team_id,team_name,active,f_name,l_name,player_name,player_number,player_pos FROM roster WHERE team_id=?"
        players_records = execute_sql_statement(self.SPORT,players_query,(team_id,))
        players = map_rows_to_players(players_records) 
        return players 

    def get_games_by_season_data(self,season_id: int):
        game_query= "SELECT season_id,game_id,team1_id,team1,team2_id,team2,date,start_time,court,playoff,played FROM schedule WHERE season_id = ?"
        games_records = execute_sql_statement(self.SPORT,game_query,(season_id,))
        games = map_row_to_games(games_records)
        return games 
   
    def get_games_by_date_data(self,date: int):
        game_query= "SELECT season_id,game_id,team1_id,team1,team2_id,team2,date,start_time,court,playoff,played FROM schedule WHERE date = ?"
        games_records = execute_sql_statement(self.SPORT,game_query,(date,))
        games = map_row_to_games(games_records)
        return games

    def get_game_ids_data(self, team_id: int):
        game_ids_query="SELECT game_id FROM games WHERE team1_id=? OR team2_id=?";
        gameID_records = execute_sql_statement(self.SPORT,game_ids_query,(team_id,team_id))
        gameIDs = [record[0] for record in gameID_records] 
        return gameIDs 

    def get_game_dates_by_season_data(self,season_id: int):
        game_day_query = "SELECT date FROM games WHERE season_id=? GROUP BY date"
        game_days_records= execute_sql_statement(self.SPORT,game_day_query,(season_id,))
        dates = [record[0] for record in game_days_records] 
        return dates
    
    def insert_players(self, roster: list[Player]):
        players_query = """
            INSERT INTO players 
                (active, f_name, l_name, name, number, pos)
            VALUES
                (?,?,?,?,?,?);
        """

        tp_query = """
            INSERT INTO teams_players 
                (team_id,player_id)
            VALUES
                (?,?);
        """
        db_url = DB_STR[self.SPORT] 
        try:
            conn = sqlite3.connect(db_url)
     
            for player in roster:
                values = (player.active, player.f_name, player.l_name, player.name, player.number, player.pos) 
                tid = player.team_id
                insert_many_to_many_query(conn, players_query,values,tp_query,tid)
            conn.commit()
        except sqlite3.Error as error:
            raise RuntimeError(f'error inserting data - {error}')
        finally:
            if conn:
                conn.close()
                print("Closing SQLite Connection")

    def update_players(self, roster: list[Player]):
        player_values = [(player.active, player.f_name, player.l_name, player.name, player.number, player.pos, player.player_id) for player in roster]
        query_update = """
            UPDATE players 
            SET active = ?,
                f_name = ?,
                l_name = ?,
                name = ?,
                number = ?,
                pos = ?
            WHERE
                id = ? 
            ORDER BY
                id
            LIMIT 1;       
        """
        execute_bulk_query(self.SPORT, query_update, player_values)
    
    @abstractmethod
    def get_player_stats_data(self,stat: Stat,season_id: int):
        pass

    @abstractmethod
    def get_teams_data(self,season_id: int):
        pass

    @abstractmethod
    def get_game_stats_data(self,game_id: int):
        pass

    @abstractmethod
    def get_game_player_stats_data(self,game_id: int):
        pass











        



