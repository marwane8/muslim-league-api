from pydantic import BaseModel 

class Player(BaseModel):
    id: int
    name: str | None = None
    number: str | None
    pos: str

class PlayerStats(BaseModel):
    id: int
    name: str | None = None
    stat: str 

class TeamRanks(BaseModel):
    id: int
    name: str | None = None
    ovr_all: int 
    points_rnk: int 
    rebound_rnk: int 

class Team(BaseModel):
    id: int
    name: str | None = None

class TeamStats(BaseModel):
    id: int
    name: str | None = None
    wins: int
    loss: int
    points_for: int
    points_against: int
    rebounds_total: int
    diff: int

class GameDates(BaseModel):
    games: list[int]

class Game(BaseModel):
    game_id: int
    team1_id: int
    team1: str
    team2_id: int
    team2: str 
    date: int
    start_time: str
    court: int
    playoff: int

class GameStats(BaseModel):
    game_id: int
    team_id: int
    team_name: str
    points: int
    rebounds: int
    fouls: int

class Season(BaseModel):
    season_id: int
    season_name: str
    year: int