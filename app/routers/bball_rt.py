from fastapi import APIRouter,Path

from app.accessors.bball_accessor import *
from app.processors.bball_processor import BasketballProcessor

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
@router.get("/teams/{season_id}" ,summary=get_teams_summary, response_model=list[Team])
def get_roster(season_id: int = Path(None,description="ID of a Season")):
    return bball_proc.get_teams(season_id) 

get_standings_summary = "Returns a sorted list of teams of a given season id according their prefomance records"
@router.get("/teams/{season_id}/standings" ,summary=get_standings_summary, response_model=list[Team])
def get_standings(season_id: int = Path(None,description="The ID of a Season")):
    return  bball_proc.get_teams(season_id)


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
get_game_summary= "Returns a list of all dates games are played in a season"
@router.get("/games/{season_id}/dates" ,summary=get_game_summary, response_model=list[int])
def get_games(season_id: int = Path(None,description="The ID of a Season")):
    return bball_proc.get_game_dates_by_season(season_id)

get_game_by_date_summary= "Returns a list of games for a given date"
@router.get("/games/{date}" ,summary=get_game_by_date_summary, response_model=list[Game])
def get_games_by_date(date: int = Path(None,description="Date fromated YYYYMMDD")):
    return bball_proc.get_games_by_date(date)

get_game_stats_summary= "Return that stat totals of each team for a game"
@router.get("/games/stats/{game_id}" ,summary=get_game_stats_summary, response_model=list[GameStats])
def get_games(game_id: int = Path(None,description="The ID of a Game")):
    #TODO: Implement in bball_proc
    return bball_proc.get_game_stats(game_id)

