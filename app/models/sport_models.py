from pydantic import BaseModel 
from enum import Enum

class Sport(Enum):
    BASKETBALL = 1
    SOCCER = 2

class Season(BaseModel):
    season_id: int
    season_name: str
    year: int

class Game(BaseModel):
    season_id: int
    game_id: int
    team1_id: int
    team1: str
    team2_id: int
    team2: str 
    date: int
    start_time: str
    court: int
    playoff: int

class GameDates(BaseModel):
    games: list[int]

class Player(BaseModel):
    player_id: int 
    team_id: int 
    team_name: str 
    name: str 
    number: str 
    pos: str

class Stat(Enum):
    pass

class PlayerStat(BaseModel):
    id: int
    name: str | None = None
    games: int
    stat: int 




