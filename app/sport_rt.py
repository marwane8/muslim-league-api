from fastapi import APIRouter,Path,Depends,HTTPException

from app.auth_deps import get_current_user

from .models.user_models import User
from .models.sport_models import *

from .processors.bball_processor import BasketBallProcessor 
from .accessors.db_accessor import Accessor


router = APIRouter(
    prefix="/api/v1",
    tags=["sport"]
)

proc = BasketBallProcessor() 
db_acc = Accessor()
#--------------
# Season API 
#--------------
get_teams_summary= "Returns a list of all available seasons"
@router.get("/seasons/{sport}" ,summary=get_teams_summary, response_model=list[Season])
def get_all_seasons(sport: str = Path(None,description="The Name of a Sport")):
    try:
        seasons = db_acc.get_seasons_data(sport)
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Endpoint Error, The Sport: {sport} was not found")


    return seasons

get_game_summary= "Returns a list of all dates games are played in a season"
@router.get("/games/{season_id}/dates" ,summary=get_game_summary, response_model=list[int])
def get_game_dates(season_id: int = Path(None,description="The ID of a Season")):
    return db_acc.get_game_dates_by_season_data(season_id)

#--------------
# Teams API 
#--------------
get_teams_summary= "Returns a list of teams associated with the given season"
@router.get("/teams/{season_id}" ,summary=get_teams_summary, response_model=list[TeamData])
def get_team_info(season_id: int = Path(None,description="ID of a Season")):
    return proc.get_teams(season_id) 

get_roster_summary = "Returns a list of players associated with the given team id"
@router.get("/players/{team_id}" ,summary=get_roster_summary, response_model=list[Player])
def get_roster(team_id: int = Path(None,description="The ID of a Team")):
    return db_acc.get_players_data(team_id) 

#--------------
# Games API Endpoints
#--------------
get_game_summary= "Returns all the games of a given season"
@router.get("/games/season/{season_id}" ,summary=get_game_summary, response_model=list[Game])
def get_game_for_season(season_id: int = Path(None,description="The ID of a Season")):
    return db_acc.get_games_by_season_data(season_id)

get_game_dates_summary= "Returns a list of all dates games are played in a season"
@router.get("/games/{season_id}/dates" ,summary=get_game_summary, response_model=list[int])
def get_game_dates(season_id: int = Path(None,description="The ID of a Season")):
    return db_acc.get_game_dates_by_season(season_id)

#--------------
# Stat API Endpoints
#--------------
get_game_team_stats_summary= "Return the stat totals of each team for a game"
@router.get("/games/stats/teams/{game_id}" ,summary=get_game_team_stats_summary, response_model=list[TeamGameStats])
def get_game_team_stats(game_id: int = Path(None,description="The ID of a Game")):
    return db_acc.get_game_totals_data([game_id])

get_stat_leaders_summary= "Returns a list of the top players of a given statistical category" 
@router.get("/players/{season_id}/stat/{category}" ,summary=get_stat_leaders_summary, response_model=list[PlayerStat])
def get_stat_leaders_summary(season_id: int = Path(None,description="The ID of a Season"),category: str= Path(None,description="Statiscal Category eg. Points, Rebounds")):
    leaders = []
    try:
        leaders = proc.get_stat_leaders(season_id,category)
    except Exception as e:
        raise HTTPException(status_code=400,detail="Endpoint Error, Stat Category was not found")


    return leaders 

get_game_player_stats_summary= "Return that individual player stats of a game"
@router.get("/games/stats/players/{game_id}" ,summary=get_game_player_stats_summary, response_model=list[PlayerGameStats])
def get_game_player_stats(game_id: int = Path(None,description="The ID of a Game")):
    return db_acc.get_game_player_stats_data(game_id)





#--------------
# Update API Endpoints
#--------------
upsert_roster_summary= "update and insert team data"
@router.put("/roster/upsert" ,summary=upsert_roster_summary)
def insert_roster(roster: list[Player],user: User = Depends(get_current_user)):
    try:
        proc.upsert_roster(roster)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

    return {"message": "SUCCESS, the roster has been updated"}


upsert_game_stats_summary= "update and insert bulk statistics"
@router.put("/stats/upsert" ,summary=upsert_game_stats_summary)
def insert_games_statistics(stats: list[StatUpsert],user: User = Depends(get_current_user)):
    try:
        proc.upsert_stats(stats)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

    return {"message": "SUCCESS, the game stats have been updated"}

update_team_stats_summary= "update teams statistics"
@router.put("/stats/teams" ,summary=upsert_game_stats_summary)
def update_team_statistics(team_ids: list[int],user: User = Depends(get_current_user)):
    try:
        for id in team_ids:
            proc.update_team_stats(id);
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

    return {"message": "SUCCESS, the teams have been updated"}