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