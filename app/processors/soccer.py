from enum import Enum
from ..accessors.soccer.soccer_accessor import *
from ..accessors.soccer.soccer_models import *


class Stat(Enum):
    GOALS = 1
    ASSISTS = 2

def get_team_standings(season_id: int) -> list[Team]:
    standings = get_teams(season_id)
    standings.sort(key=lambda team: (-team.points))
    return standings

def get_stat_leaders(stat: Stat,season_id: int) -> list[PlayerTotals]:
    player_totals = get_player_totals(season_id)
    if stat == Stat.GOALS:
        player_totals.sort(key=lambda total: (-total.goals))
    elif stat == Stat.ASSISTS:
        player_totals.sort(key=lambda total: (-total.assists))
    else:
        player_totals = []
    return player_totals[:10]