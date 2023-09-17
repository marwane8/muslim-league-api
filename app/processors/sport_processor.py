from ..models.sport_models import Sport, Player, Stat
from abc import ABC, abstractmethod

class SportProcessor(ABC):
    @abstractmethod
    def get_seasons(self):
        pass

    @abstractmethod
    def get_teams(self,season_id: int):
        pass

    @abstractmethod
    def get_players(self,team_id: int):
        pass
   
    @abstractmethod
    def get_games_for_season(self,season_id: int):
        pass

    @abstractmethod
    def get_game_dates_by_season(self,season_id: int):
        pass

    @abstractmethod
    def get_games_by_date(self,date: int):
        pass

    @abstractmethod
    def get_game_stats(self,game_id: int):
        pass

    @abstractmethod
    def get_game_player_stats(self, game_id: int):
        pass

    @abstractmethod
    def get_stat_leaders(self, stat: Stat, season_id: int):
        pass

    def upsert_roster(self, roster: list[Player], season_id: int):
        in_teams = []
        up_teams = []
        for player in roster:
            if player.player_id:
                up_teams.append(player)
                continue
            in_teams.append(player)
        
