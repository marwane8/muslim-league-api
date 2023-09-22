from itertools import groupby
from operator import attrgetter

from app.models.bball_models import GameStats, BballTeamStats


def get_team_records(team_id, team_game_stats: list[GameStats]):
    grouped_stats = group_game_stats_by_game_id(team_game_stats)
    stats = BballTeamStats(
        wins=0,
        losses=0,
        points_for=0,
        points_against=0,
        rebounds=0,
        fouls=0
    )

    for teams in grouped_stats.values():
        diff = 0
        for team in teams:
            if team.team_id == team_id:
                diff += team.points
                stats.points_for += team.points
                stats.rebounds += team.rebounds
                stats.fouls += team.fouls
            else:
                diff -= team.points
                stats.points_against += team.points
        if diff > 0:
            stats.wins += 1
        else:
            stats.losses += 1
    return stats 

def group_game_stats_by_game_id(game_stats_list) -> dict[int, list[GameStats]]:
    # Sort the list by game_id
    sorted_stats = sorted(game_stats_list, key=attrgetter('game_id'))
    
    # Group the sorted list by game_id
    grouped_stats = {}
    for game_id, stats_group in groupby(sorted_stats, key=attrgetter('game_id')):
        grouped_stats[game_id] = list(stats_group)
    
    return grouped_stats