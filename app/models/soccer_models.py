from .sport_models import Stat
from pydantic import BaseModel 
from enum import Enum

class SoccerStat(Enum):
    GOALS = 1
    ASSISTS = 2

class Team(BaseModel):
    team_id: int
    season_id: int
    team_name: str
    team_captain: str 
    wins: int
    losses: int
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

class GameStat(BaseModel):
    game_id: int
    player_id: int
    goals: int
    assists: int