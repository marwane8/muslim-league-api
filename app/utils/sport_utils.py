from itertools import groupby
from operator import attrgetter

from app.models.sport_models import TeamGameStats

def group_game_stats_by_game_id(game_stats_list) -> dict[int, list[TeamGameStats]]:
    # Sort the list by game_id
    sorted_stats = sorted(game_stats_list, key=attrgetter('g_id'))
    
    # Group the sorted list by game_id
    grouped_stats = {}
    for game_id, stats_group in groupby(sorted_stats, key=attrgetter('g_id')):
        grouped_stats[game_id] = list(stats_group)
    
    return grouped_stats

