from ..accessors.soccer.soccer_accessor import get_teams
from ..accessors.soccer.soccer_models import Team

def get_team_standings(season_id: int) -> list[Team]:
    standings = get_teams(season_id)
    standings.sort(key=lambda team: (-team.points))
    return standings