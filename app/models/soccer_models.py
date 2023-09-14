from .sport_models import Stat
from pydantic import BaseModel 
from enum import Enum

class SoccerStat(Enum):
    GOALS = 1
    ASSISTS = 2

class SoccerTeamData(BaseModel):
    team_id: int
    season_id: int
    team_name: str
    team_captain: str 
    wins: int
    loss: int
    draws: int
    goals_for: int
    goals_against: int
    points: int

class GameStats(BaseModel):
    game_id: int
    team_id: int
    team_name: str
    goals: int
    assists: int

class PlayerGameStats(BaseModel):
    game_id: int
    team_id: int
    team_name: str
    player_id: int
    stat_id: int
    player_name: str
    dnp: int
    goals: int
    assists: int

class SoccerStatUpsert(BaseModel):
    stat_id: int | None
    game_id: int
    player_id: int
    dnp: int
    goals: int
    assists: int