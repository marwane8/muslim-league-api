from .sport_models import Stat
from pydantic import BaseModel 

class BballStat(Stat):
    POINTS = 1
    REBOUNDS = 2

class TeamRanks(BaseModel):
    id: int
    name: str | None = None
    ovr_all: int 
    points_rnk: int 
    rebound_rnk: int 

class BBallTeamData(BaseModel):
    team_id: int
    season_id: int
    team_name: str | None = None
    team_captain: str | None = None
    wins: int
    loss: int
    points_for: int
    points_against: int
    rebounds_total: int

class GameStats(BaseModel):
    game_id: int
    team_id: int
    team_name: str
    points: int
    rebounds: int
    fouls: int

class PlayerGameStats(BaseModel):
    game_id: int
    team_id: int
    team_name: str
    player_id: int
    stat_id: int
    player_name: str
    dnp: int
    points: int
    rebounds: int
    fouls: int

class BballStatUpsert(BaseModel):
    stat_id: int | None
    game_id: int
    player_id: int
    dnp: int
    points: int
    rebounds: int
    fouls: int