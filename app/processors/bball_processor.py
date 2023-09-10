from .sport_processor import SportProcessor

from ..accessors.bball_accessor import BasketballAccessor
from ..models.bball_models import *
from ..models.sport_models import *




class BasketballProcessor(SportProcessor):
    def __init__(self):
        self.db_accessor = BasketballAccessor()
    
    def get_seasons(self):
        return self.db_accessor.get_seasons_data()

    def get_teams(self,season_id: int):
        teams = self.db_accessor.get_teams_data(season_id)
        teams.sort(key=lambda team: (-team.wins))
        return teams

    def get_players(self,team_id: int):
        return self.db_accessor.get_players_data(team_id)
   
    def get_games_for_season(self, season_id: int):
        return self.db_accessor.get_games_by_season_data(season_id)

    def get_game_dates_by_season(self,season_id: int):
        return self.db_accessor.get_game_dates_by_season_data(season_id)
   
    def get_game_ids_by_season(self,season_id: int):
        return self.db_accessor.get_game_ids_by_season_data(season_id)
 
    def get_games_by_date(self,date: int):
        return self.db_accessor.get_games_by_date_data(date)

    def get_game_stats(self,game_id: int):
        return self.db_accessor.get_game_stats_data(game_id)
    
    def get_stat_leaders(self, stat: BballStat, season_id: int):
        stat_leaders = self.db_accessor.get_player_stats_data(stat,season_id)
        stat_leaders.sort(key=lambda player: (-player.stat))
        return stat_leaders[:10]

