from .soccer_models import Team

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

