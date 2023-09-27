import sqlite3
import json

from .mapper import *
from ..utils.db_utils import DB_URL, execute_sql_statement, commit_sql_statement, execute_bulk_query, insert_many_to_many_query


class Accessor():
    def __init__(self):
        self.stat_lookup = {}
        self.sport_lookup = {}

        self.init_stat_lookup() 
        self.init_sport_lookup()

    
    def init_stat_lookup(self):
        stat_type_qry = "SELECT id, stat FROM stat_type"
        records = execute_sql_statement(stat_type_qry)
        for stat in records:
            self.stat_lookup[stat[1]] = stat[0]
            self.stat_lookup[stat[0]] = stat[1]

    def init_sport_lookup(self):
        sport_qry = "SELECT id, name FROM sport"
        records = execute_sql_statement(sport_qry)
        for sport in records:
            self.sport_lookup[sport[0]] = sport[1]
            self.sport_lookup[sport[1]] = sport[0]


    def get_seasons_data(self, sport=None):
        season_query = "SELECT id, sport_id, name, year FROM seasons"

        sport_id=self.sport_lookup[sport]
        season_query = "SELECT id, sport_id, name, year FROM seasons WHERE sport_id=?"

        season_records = execute_sql_statement(season_query,(sport_id,))
        season = map_rows_to_seasons(season_records)
        return season 

    def get_game_dates_by_season_data(self,season_id: int):
        game_day_query = "SELECT date FROM games WHERE season_id=? GROUP BY date"
        game_days_records= execute_sql_statement(game_day_query,(season_id,))
        dates = [record[0] for record in game_days_records] 
        return dates

    def get_games_by_date(self, date: int):
        game_query= "SELECT sport_id,season_id,game_id,team1_id,team1,team2_id,team2,date,start_time,court,playoff,played FROM schedule WHERE date = ?"
        games_records = execute_sql_statement(game_query,(date,))
        games = map_row_to_games(games_records)
        return games 
 
    def get_teams_data(self,season_id: int):
        teams_query = "SELECT id, season_id, name, captain_id, stats_obj FROM teams WHERE season_id=?"
        teams_records = execute_sql_statement(teams_query,(season_id,))
        teams = map_row_to_team(teams_records) 
        return teams

    def get_players_data(self,team_id: int):
        players_query = "SELECT id,team_id,team_name,active,f_name,l_name,player_name,player_number,player_pos FROM roster WHERE team_id=?"
        players_records = execute_sql_statement(players_query,(team_id,))
        players = map_rows_to_players(players_records) 
        return players 

    def get_stat_leaders_data(self, season_id: int, stat_id: int):
        query1 = "SELECT season_id, p_id, name, stat_records, dnp, type1, stat1 FROM player_totals WHERE season_id = ? AND type1 = ?"
        query2 = "SELECT season_id, p_id, name, stat_records, dnp, type2, stat2 FROM player_totals WHERE season_id = ? AND type2 = ?"
        query3 = "SELECT season_id, p_id, name, stat_records, dnp, type3, stat3 FROM player_totals WHERE season_id = ? AND type3 = ?"
        stat_qrys = [query1,query2,query3]
        games_records = []
        for query in stat_qrys:
            records = execute_sql_statement(query,(season_id,stat_id))
            games_records+=records
        category = self.stat_lookup[stat_id]
        games = map_row_to_stat(games_records,category)
        return games

    def get_games_by_season_data(self,season_id: int):
        game_query= "SELECT sport_id,season_id,game_id,team1_id,team1,team2_id,team2,date,start_time,court,playoff,played FROM schedule WHERE season_id = ?"
        games_records = execute_sql_statement(game_query,(season_id,))
        games = map_row_to_games(games_records)
        return games 
   
    def get_game_dates_by_season(self,season_id: int):
        game_day_query = "SELECT date FROM games WHERE season_id=? GROUP BY date"
        game_days_records= execute_sql_statement(game_day_query,(season_id,))
        dates = [record[0] for record in game_days_records] 
        return dates

    def get_game_ids(self, team_id: int):
        game_ids_query="SELECT id FROM games WHERE team1_id=? OR team2_id=?";
        gameID_records = execute_sql_statement(game_ids_query,(team_id,team_id))
        gameIDs = [record[0] for record in gameID_records] 
        return gameIDs 

    def get_game_totals_data(self, gameIDs: list[int]):
        placeholders = ','.join(['?'] * len(gameIDs))
        game_stats_query= f"SELECT t_id, team_name, g_id, type1, stat1_total, type2, stat2_total, type3, stat3_total FROM game_totals WHERE g_id IN ({placeholders})"
        games_records = execute_sql_statement(game_stats_query,gameIDs)
        games = map_row_to_game_totals(games_records,self.stat_lookup)
        return games


    def get_game_player_stats_data(self, game_id: int):
        game_stats_query= "SELECT game_id, team_id, team_name, player_id, stat_id, player_name, type1, stat1, type2, stat2, type3, stat3 FROM game_statistics WHERE game_id = ?"
        games_records = execute_sql_statement(game_stats_query,(game_id,))
        games = map_row_to_player_game_stats(games_records,self.stat_lookup)
        return games

    #--------------
    # Insert and Update Logic
    #--------------
    def update_team_stats_obj(self, team_id, stats_obj: dict):
        stats_str = json.dumps(stats_obj)
        query_update = """
            UPDATE teams 
            SET stats_obj = ?
            WHERE
                id = ? 
            ORDER BY
                id
            LIMIT 1;       
        """
        commit_sql_statement(query_update, [stats_str, team_id])


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

        try:
            conn = sqlite3.connect(DB_URL)
     
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
        execute_bulk_query(query_update, player_values)
 
    def insert_stats(self, stats: list[StatUpsert]):
        stat_values = [(stat.sport_id, stat.game_id, stat.player_id, stat.dnp, stat.stat1_type, stat.stat1, stat.stat2_type, stat.stat2, stat.stat3_type, stat.stat3) for stat in stats]
        query_insert = """
        INSERT INTO statistics ( sport_id, game_id, player_id, dnp, stat1_type, stat1, stat2_type, stat2, stat3_type, stat3 )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        execute_bulk_query(query_insert,stat_values)



    def update_stats(self, stats: list[StatUpsert]):
        stat_values = [(stat.id, stat.sport_id, stat.game_id, stat.player_id, stat.dnp, stat.stat1_type, stat.stat1, stat.stat2_type, stat.stat2, stat.stat3_type, stat.stat3) for stat in stats]
        query_update = """
            UPDATE statistics 
            SET id = ?,
                sport_id = ?,
                game_id = ?,
                player_id = ?,
                dnp = ?,
                stat1_type = ?,
                stat1 = ?,
                stat2_type = ?,
                stat2 = ?,
                stat3_type = ?,
                stat3 = ?
            WHERE
                stat_id = ? 
            ORDER BY
                stat_id
            LIMIT 1;       
        """
        execute_bulk_query( query_update, stat_values)
