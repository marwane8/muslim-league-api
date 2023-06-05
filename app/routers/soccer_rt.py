from fastapi import APIRouter,Path

from app.accessors.soccer.soccer_models import *
from app.processors.soccer import *

router = APIRouter(
    prefix="/api/v1/soccer",
    tags=["soccer"]
)

#--------------
# Team API Endpoints
#--------------
get_teams_summary= "Returns a list of teams associated with the given season"
@router.get("/teams/{season_id}" ,summary=get_teams_summary, response_model=list[Team])
def get_teams_by_season(season_id: int = Path(None,description="ID of a Season")):
    teams = get_teams(season_id)
    return teams 


get_standings_summary = "Returns a sorted list of teams of a given season id according their prefomance records"
@router.get("/teams/{season_id}/standings" ,summary=get_standings_summary, response_model=list[Team])
def get_standings(season_id: int = Path(None,description="The ID of a Season")):
    return get_teams(season_id,SortBy.STANDINGS)


#--------------
# Player API Endpoints
#--------------
get_players_summary = "Returns a list of players associated with the given team id"
@router.get("/players/{team_id}" ,summary=get_players_summary, response_model=list[Player])
def get_players(team_id: int = Path(None,description="The ID of a Team")):
    players = get_players_by_team(team_id)
    return players 


get_stat_leaders_summary= "Returns a list of the top players of a given statistical category" 
@router.get("/players/{season_id}/stat/{category}" ,summary=get_stat_leaders_summary, response_model=list[PlayerTotals])
def get_stat_leaders_summary(season_id: int = Path(None,description="The ID of a Season"),category: str= Path(None,description="Statiscal Category eg. goals, assists")):
    match category:
        case "goals":
            return  get_stat_leaders(Stat.GOALS,season_id)
        case "assists":
            return  get_stat_leaders(Stat.ASSISTS,season_id)
    return [] 

