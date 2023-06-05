from .soccer_models import *

def map_rows_to_teams(rows) -> list[Team]:
    teams = []
    for row in rows:
        team_id,season_id,team_name,team_captain,wins,losses,draws,goals_for,goals_against,points = row
        team = Team(
            team_id=team_id,
            season_id=season_id,
            team_name=team_name,
            team_captain=team_captain,
            wins=wins,
            losses=losses,
            draws=draws,
            goals_for=goals_for,
            goals_against=goals_against,
            points=points
        )
        teams.append(team)
    return teams


def map_rows_to_players(rows) -> list[Player]:
    players = []
    for row in rows:
        player_id,team_id,team_name,player_name,player_number,player_pos  = row
        player = Player(
            player_id=player_id,
            team_id=team_id,
            team_name=team_name,
            player_name=player_name,
            player_number=player_number,
            player_pos=player_pos
        )
        players.append(player)
    return players

def map_rows_to_player_totals(rows) -> list[PlayerTotals]:
    player_totals = []
    for row in rows:
        player_id, player_name, games_played, goals, assists = row
        team = PlayerTotals(
            player_id=player_id,
            player_name=player_name,
            games_played=games_played,
            goals=goals,
            assists=assists
        )
        player_totals.append(team)
    return player_totals