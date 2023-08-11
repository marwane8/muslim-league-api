#basketball processor logic here
from ..accessors.bball.bball_accessor import *

def get_seasons():
    seasons = get_seasons_data()
    return seasons 

def get_stat_leaders(stat: Stat,season_id: int) -> list[PlayerStats]:
    player_totals = []
    if stat == Stat.POINTS:
        player_totals = get_stat_leaders_data(Stat.POINTS,season_id)
    elif stat == Stat.REBOUNDS:
        player_totals = get_stat_leaders_data(Stat.REBOUNDS,season_id)

    player_totals.sort(key=lambda player: (-player.stat))

    return player_totals[:10]


