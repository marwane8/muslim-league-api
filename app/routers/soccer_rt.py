from fastapi import APIRouter,Path

from app.accessors.soccer.soccer_models import *
from app.processors.soccer import get_team_standings

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
    standings = get_team_standings(season_id)
    return standings 


