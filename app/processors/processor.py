import abc

from app.accessors.db_accessor import Accessor 
from app.models.sport_models import *

class Processor(abc.ABC):
    def __init__(self):
        self.db_accessor = Accessor()
    
    def get_teams(self,season_id: int):
        teams = self.db_accessor.get_teams_data(season_id)
        # TODO: fix json object team sort
        # teams.sort(key=lambda team: (-team.wins))
        return teams

    def get_stat_leaders(self, season_id: int, category: str):
        stat_id = self.db_accessor.stat_lookup[category]
        stat_leaders: list[PlayerStat] = self.db_accessor.get_stat_leaders_data(season_id, stat_id)
        stat_leaders.sort(key=lambda p_stat : -p_stat.stat)
        return stat_leaders[:10]
       
    #--------------
    # Insert and Update Logic
    #--------------
    def upsert_roster(self, roster: list[Player]):
        in_team = []
        up_team = []
        for player in roster:
            if player.player_id:
                up_team.append(player)
                continue
            in_team.append(player)
        self.db_accessor.insert_players(in_team)
        self.db_accessor.update_players(up_team)
 
    def upsert_stats(self, stats: [StatUpsert]):
        in_stats = []
        up_stats = []
        for stat in stats:
            if stat.id:
                up_stats.append(stat)
                continue
            in_stats.append(stat)
        self.db_accessor.insert_stats(in_stats)
        self.db_accessor.update_stats(up_stats)
 

    def update_team_stats(self, team_id: int):
        gameIDs = self.db_accessor.get_game_ids(team_id)
        team_game_stats = self.db_accessor.get_game_totals_data(gameIDs)
        stats_dict = self.calculate_team_stats(team_id, team_game_stats)
        self.db_accessor.update_team_stats_obj(team_id, stats_dict)
        return stats_dict 

    @abc.abstractclassmethod
    def calculate_team_stats(self, team_id, team_game_stats: list[TeamGameStats]):
        pass


   