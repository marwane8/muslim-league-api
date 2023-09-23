import sqlite3

from ..models.sport_models import Sport, Stat
from ..mappers.sport_mapper import *
from ..db_utils import DB_URL, execute_sql_statement, execute_bulk_query, insert_many_to_many_query


class Accessor():
    def __init__(self):
        self.stat_lookup = self.init_stat_lookup() 
        self.sport_lookup = self.init_sport_lookup() 
    
    def init_stat_lookup(self):
        stat_lookup = {}
        stat_type_qry = "SELECT id, stat FROM stat_type"
        records = execute_sql_statement(stat_type_qry)
        for stat in records:
            stat_lookup[stat[0]] = stat[1]
        return stat_lookup 

    def init_sport_lookup(self):
        sport_lookup = {}
        sport_qry = "SELECT id, name FROM sport"
        records = execute_sql_statement(sport_qry)
        for sport in records:
            sport_lookup[sport[0]] = sport[1]
        return sport_lookup 


    def get_seasons_data(self, sport_id=None):
        season_query = "SELECT id, sport_id, name, year FROM seasons"
        value=None
        if sport_id:
            season_query = "SELECT id, sport_id, name, year FROM seasons WHERE sport_id=?"
            value=[sport_id]

        season_records = execute_sql_statement(season_query,value)
        season = map_rows_to_seasons(season_records)
        return season 
