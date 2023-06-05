from fastapi import APIRouter,Path

from app.accessors.soccer.soccer_models import *
from app.processors.soccer import *

router = APIRouter(
    prefix="/api/v1/soccer",
    tags=[""]
)

#--------------
# Team API Endpoints
#--------------
get_standings_summary = "Returns a sorted list of teams of a given season id according their prefomance records"
@router.get("/teams/{season_id}/standings" ,summary=get_standings_summary, response_model=list[Team])
def get_standings(season_id: int = Path(None,description="The ID of a Season")):
    return get_team_standings(season_id)


#--------------
# Player API Endpoints
#--------------
get_stat_leaders_summary= "Returns a list of the top players of a given statistical category" 
@router.get("/players/{season_id}/stat/{category}" ,summary=get_stat_leaders_summary, response_model=list[PlayerTotals])
def get_stat_leaders_summary(season_id: int = Path(None,description="The ID of a Season"),category: str= Path(None,description="Statiscal Category eg. goals, assists")):
    match category:
        case "goals":
            return  get_stat_leaders(Stat.GOALS,season_id)
        case "assists":
            return  get_stat_leaders(Stat.ASSISTS,season_id)
    return [] 

