from fastapi import APIRouter,Path,Depends,HTTPException

from app.auth_deps import get_current_user
from app.accessors.bball_accessor import *
from app.processors.bball_processor import BasketballProcessor

from ..models.user_models import User
from ..models.bball_models import *
from ..models.sport_models import *


router = APIRouter(
    prefix="/api/v1/bball",
    tags=["bball"]
)

bball_proc = BasketballProcessor()
#--------------
# Season API Endpoints
#--------------
get_teams_summary= "Returns a list of all available seasons"
@router.get("/seasons" ,summary=get_teams_summary, response_model=list[Season])
def get_all_seasons():
    return bball_proc.get_seasons()


#-------------
# Team API Endpoints
#--------------
get_teams_summary= "Returns a list of teams associated with the given season"
@router.get("/teams/{season_id}" ,summary=get_teams_summary, response_model=list[BBallTeamData])
def get_roster(season_id: int = Path(None,description="ID of a Season")):
    return bball_proc.get_teams(season_id) 


#--------------
# Player API Endpoints
#--------------
get_roster_summary = "Returns a list of players associated with the given team id"
@router.get("/players/{team_id}" ,summary=get_roster_summary, response_model=list[Player])
def get_roster(team_id: int = Path(None,description="The ID of a Team")):
    return bball_proc.get_players(team_id) 

get_stat_leaders_summary= "Returns a list of the top players of a given statistical category" 
@router.get("/players/{season_id}/stat/{category}" ,summary=get_stat_leaders_summary, response_model=list[PlayerStat])
def get_stat_leaders_summary(season_id: int = Path(None,description="The ID of a Season"),category: str= Path(None,description="Statiscal Category eg. Points, Rebounds")):
    match category:
        case "points":
            return bball_proc.get_stat_leaders(BballStat.POINTS,season_id)
        case "rebounds":
            return bball_proc.get_stat_leaders(BballStat.REBOUNDS,season_id)
    return [] 

#--------------
# Games API Endpoints
#--------------
get_game_summary= "Returns all the games of a given season"
@router.get("/games/season/{season_id}" ,summary=get_game_summary, response_model=list[Game])
def get_game_for_season(season_id: int = Path(None,description="The ID of a Season")):
    return bball_proc.get_games_for_season(season_id)


get_game_summary= "Returns a list of all dates games are played in a season"
@router.get("/games/{season_id}/dates" ,summary=get_game_summary, response_model=list[int])
def get_game_dates(season_id: int = Path(None,description="The ID of a Season")):
    return bball_proc.get_game_dates_by_season(season_id)

get_game_by_date_summary= "Returns a list of games for a given date"
@router.get("/games/{date}" ,summary=get_game_by_date_summary, response_model=list[Game])
def get_games_by_date(date: int = Path(None,description="Date fromated YYYYMMDD")):
    return bball_proc.get_games_by_date(date)

get_game_stats_summary= "Return the stat totals of each team for a game"
@router.get("/games/stats/teams/{game_id}" ,summary=get_game_stats_summary, response_model=list[GameStats])
def get_game_stats(game_id: int = Path(None,description="The ID of a Game")):
    return bball_proc.get_game_stats(game_id)

get_game_player_stats_summary= "Return that individual player stats of a game"
@router.get("/games/stats/players/{game_id}" ,summary=get_game_player_stats_summary, response_model=list[PlayerGameStats])
def get_game_player_stats(game_id: int = Path(None,description="The ID of a Game")):
    return bball_proc.get_game_player_stats(game_id)

upsert_roster_summary= "update and insert  team data"
@router.put("/roster/upsert" ,summary=upsert_roster_summary)
def insert_games_statistics(roster: list[Player],user: User = Depends(get_current_user)):
    try:
        bball_proc.upsert_roster(roster)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

    return {"message": "SUCESS - stats updated"}


upsert_game_stats_summary= "update and insert bulk statistics"
@router.put("/stats/upsert" ,summary=upsert_game_stats_summary)
def insert_games_statistics(stats: list[BballStatUpsert],user: User = Depends(get_current_user)):
    try:
        bball_proc.upsert_stats(stats)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

    return {"message": "SUCESS - stats updated"}

update_team_stats_summary= "update teams statistics"
@router.put("/stats/teams" ,summary=upsert_game_stats_summary)
def insert_games_statistics(team_ids: list[int],user: User = Depends(get_current_user)):
    try:
        for id in team_ids:
            bball_proc.update_team_stats(id);
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

    return {"message": "SUCESS - stats updated"}