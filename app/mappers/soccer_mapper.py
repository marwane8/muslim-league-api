from ..models.soccer_models import *

def map_rows_to_teams(rows) -> list[SoccerTeamData]:
    teams = []
    for row in rows:
        team_id,season_id,team_name,team_captain,wins,losses,draws,goals_for,goals_against,points = row
        team = SoccerTeamData(
            team_id=team_id,
            season_id=season_id,
            team_name=team_name,
            team_captain=team_captain,
            wins=wins,
            loss=losses,
            draws=draws,
            goals_for=goals_for,
            goals_against=goals_against,
            points=points
        )
        teams.append(team)
    return teams



def map_row_to_soccer_game_stats(records: list[tuple]) -> list[GameStats]:
    game_stats = []
    if records == []:
        print("Not teams found for requested season")
    else:
        for game_data in records:
            g_id,t_id,team_name,goals,assists = game_data[:6] 
            game = GameStats(
                 game_id=g_id,
                 team_id=t_id,
                 team_name=team_name,
                 goals=goals,
                 assists=assists
            )
            game_stats.append(game)

    return game_stats

