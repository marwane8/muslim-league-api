
from app.models.sport_models import TeamGameStats, TeamData, BballStandings
from .processor import Processor
from ..utils.sport_utils import group_game_stats_by_game_id
from ..accessors.mapper import map_teams_to_ball_standings

class BasketBallProcessor(Processor):

    def get_standings(self, season_id):
        teams: list[TeamData] = self.db_accessor.get_teams_data(season_id)
        standings = map_teams_to_ball_standings(teams)
        standings.sort(key=lambda team: (team.wins, (team.points_for - team.points_against)), reverse=True)
        return standings 

    def calculate_team_stats(self, team_id, team_game_stats: list[TeamGameStats]):
        grouped_stats = group_game_stats_by_game_id(team_game_stats)
        stats = {
            "wins": 0,
            "losses": 0,
            "points_for": 0,
            "points_against":0,
            "rebounds":0,
            "fouls":0
        }
        
        for teams in grouped_stats.values():
            diff = 0
            for team in teams:
                if team.t_id == team_id:
                    diff += team.stat1_total
                    stats["points_for"] += team.stat1_total
                    stats["rebounds"] += team.stat2_total
                    stats["fouls"] += team.stat3_total
                else:
                    diff -= team.stat1_total
                    stats["points_against"] += team.stat1_total
            if diff > 0:
                stats["wins"] += 1
            else:
                stats["losses"] += 1
        return stats

