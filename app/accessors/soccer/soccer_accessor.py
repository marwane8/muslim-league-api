from .soccer_mapper import *
from .soccer_models import Team
from ..db_utils import DB,execute_sql_statement,fetchone_sql_statement,commit_sql_statement

#--------------
# Teams Functions 
#--------------
def get_teams(season_id: int) -> list[Team]:
    teams_query = "SELECT team_id, season_id, team_name, team_captain, wins, losses, draws, goals_for, goals_against, points FROM Teams WHERE season_id=?"
    teams_records = execute_sql_statement(DB.SOCCER,teams_query,(season_id,))
    teams = map_rows_to_teams(teams_records) 
    return teams


