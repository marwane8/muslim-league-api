from enum import Enum
from ..accessors.soccer.soccer_accessor import *
from ..accessors.soccer.soccer_models import *



class SortBy(Enum):
    ROSTER = 1
    STANDINGS = 2

def get_teams(season_id: int, sorter: SortBy=SortBy.ROSTER) -> list[Team]:
    standings = get_teams_data(season_id)
    if sorter== SortBy.STANDINGS:
        standings.sort(key=lambda team: (-team.points))
    else:
        standings.sort(key=lambda team: (team.team_id))
    return standings


def get_players_by_team(team_id: int):
    players = get_players_data(team_id)
    return players


class Stat(Enum):
    GOALS = 1
    ASSISTS = 2

def get_stat_leaders(stat: Stat,season_id: int) -> list[PlayerTotals]:
    player_totals = get_player_totals_data(season_id)
    if stat == Stat.GOALS:
        player_totals.sort(key=lambda total: (-total.goals))
    elif stat == Stat.ASSISTS:
        player_totals.sort(key=lambda total: (-total.assists))
    else:
        player_totals = []
    return player_totals[:10]


def get_games_dates_by_season(season_id: int) -> list[int]:
    games = get_game_dates(season_id)
    return games

def get_games_stats(game_id: int) -> list[GameStats]:
    game_stats = get_game_stats_data(game_id)
    return game_stats