from fastapi import APIRouter,Path

from app.accessors.bball.bball_accessor import *
from app.processors.bball import *

router = APIRouter(
    prefix="/api/v1/bball",
    tags=["bball"]
)
#--------------
# Season API Endpoints
#--------------
get_teams_summary= "Returns a list of all available seasons"
@router.get("/seasons" ,summary=get_teams_summary, response_model=list[Season])
def get_all_seasons():
    seasons = get_seasons()
    return seasons 


#-------------
# Team API Endpoints
#--------------
get_teams_summary= "Returns a list of teams associated with the given season"
@router.get("/teams/{season_id}" ,summary=get_teams_summary, response_model=list[Team])
def get_roster(season_id: int = Path(None,description="ID of a Season")):
    teams = get_all_teams(season_id)
    return teams 

get_standings_summary = "Returns a sorted list of teams of a given season id according their prefomance records"
@router.get("/teams/{season_id}/standings" ,summary=get_standings_summary, response_model=list[TeamStats])
def get_standings(season_id: int = Path(None,description="The ID of a Season")):
    standings = get_team_standings(season_id)
    return standings 


#--------------
# Player API Endpoints
#--------------
get_roster_summary = "Returns a list of players associated with the given team id"
@router.get("/players/{team_id}" ,summary=get_roster_summary, response_model=list[Player])
def get_roster(team_id: int = Path(None,description="The ID of a Team")):
    roster = get_team_roster(team_id)
    return roster 

get_stat_leaders_summary= "Returns a list of the top players of a given statistical category" 
@router.get("/players/{season_id}/stat/{category}" ,summary=get_stat_leaders_summary, response_model=list[PlayerStats])
def get_stat_leaders_summary(season_id: int = Path(None,description="The ID of a Season"),category: str= Path(None,description="Statiscal Category eg. Points, Rebounds")):
    match category:
        case "points":
            return get_stat_leaders(Stat.POINTS,season_id)
        case "rebounds":
            return get_stat_leaders(Stat.REBOUNDS,season_id)
    return [] 

#--------------
# Games API Endpoints
#--------------
get_game_summary= "Returns a list of all the dates games are played in the database"
@router.get("/games/dates" ,summary=get_game_summary, response_model=GameDates)
def get_games():
    game_days = get_game_days()
    return game_days 

get_game_by_date_summary= "Returns a list of games for a given date"
@router.get("/games/{date}" ,summary=get_game_summary, response_model=list[Game])
def get_games_by_date(date: int = Path(None,description="Date fromated YYYYMMDD")):
    games = get_games_of_date(date)
    return games

get_game_stats_summary= "get all statistics of each game"
@router.get("/games/stats/{game_id}" ,summary=get_game_stats_summary, response_model=list[GameStats])
def get_games_statistics(game_id: int = Path(None,description="ID for game")):
    game_stats = get_games_stats(game_id)
    return game_stats