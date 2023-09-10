from fastapi import APIRouter,Path, HTTPException, Depends
from app.auth_deps import get_current_user
from app.models.user_models import User

from app.models.sport_models import *
from ..models.soccer_models import *
from app.processors.soccer_processor import SoccerProcessor


router = APIRouter(
    prefix="/api/v1/soccer",
    tags=["soccer"]
)

soccer_proc = SoccerProcessor()
#--------------
# Season API Endpoints
#--------------
get_teams_summary= "Returns a list of all available seasons"
@router.get("/seasons" ,summary=get_teams_summary, response_model=list[Season])
def get_all_seasons():
    return soccer_proc.get_seasons() 

#--------------
# Team API Endpoints
#--------------
get_teams_summary= "Returns a list of teams associated with the given season"
@router.get("/teams/{season_id}" ,summary=get_teams_summary, response_model=list[SoccerTeamData])
def get_teams_by_season(season_id: int = Path(None,description="ID of a Season")):
    return soccer_proc.get_teams(season_id)


#--------------
# Player API Endpoints
#--------------
get_players_summary = "Returns a list of players associated with the given team id"
@router.get("/players/{team_id}" ,summary=get_players_summary, response_model=list[Player])
def get_team_players(team_id: int = Path(None,description="The ID of a Team")):
    return soccer_proc.get_players(team_id)



get_stat_leaders_summary= "Returns a list of the top players of a given statistical category" 
@router.get("/players/{season_id}/stat/{category}" ,summary=get_stat_leaders_summary, response_model=list[PlayerStat])
def get_stat_leaders_summary(season_id: int = Path(None,description="The ID of a Season"),category: str= Path(None,description="Statiscal Category eg. goals, assists")):
    match category:
        case "goals":
            return  soccer_proc.get_stat_leaders(SoccerStat.GOALS,season_id)
        case "assists":
            return  soccer_proc.get_stat_leaders(SoccerStat.ASSISTS,season_id)
    return [] 


#--------------
# Game API Endpoints
#--------------
get_game_summary= "Returns all the games of a given season"
@router.get("/games/season/{season_id}" ,summary=get_game_summary, response_model=list[Game])
def get_game_for_season(season_id: int = Path(None,description="The ID of a Season")):
    return soccer_proc.get_games_for_season(season_id)


get_game_dates_summary= "Returns a list of all the dates games are played in the database"
@router.get("/games/{season_id}/dates" ,summary=get_game_dates_summary, response_model=list[int])
def get_games_dates(season_id: int = Path(None,description="The ID of a Season")):
    game_dates = soccer_proc.get_game_dates_by_season(season_id) 
    return game_dates

get_game_by_date_summary= "Returns a list of games for a given date"
@router.get("/games/{date}" ,summary=get_game_by_date_summary, response_model=list[Game])
def get_games_by_date(date: int = Path(None,description="Date fromated YYYYMMDD")):
    return soccer_proc.get_games_by_date(date)

#--------------
# Admin Endpoints 
#--------------
get_game_stats_summary= "Return the stat totals of each team for a game"
@router.get("/games/stats/teams/{game_id}" ,summary=get_game_stats_summary, response_model=list[GameStats])
def get_games_statistics(game_id: int = Path(None,description="ID for game")):
    game_stats = soccer_proc.get_game_stats(game_id)
    return game_stats

get_game_player_stats_summary= "Return that individual player stats of a game"
@router.get("/games/stats/players/{game_id}" ,summary=get_game_player_stats_summary, response_model=list[PlayerGameStats])
def get_game_player_stats(game_id: int = Path(None,description="The ID of a Game")):
    return soccer_proc.get_game_player_stats(game_id)



insert_game_stats_summary= "insert statistics bulk statistics"
@router.put("/stats/insert" ,summary=get_game_stats_summary)
def insert_games_statistics(stats: list[SoccerStat],user: User = Depends(get_current_user)):
    try:
        insert_soccer_stats(stats)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

    return {"message": "Stats updated successfully."}


