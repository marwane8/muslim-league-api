from pydantic import BaseModel 

class TokenSchema(BaseModel):
    access_token: str

class TokenPayload(BaseModel):
    exp: int = None
    sub: str = None
    admin: bool = False 

class User(BaseModel):
    username: str
    password: str | None = None
    admin: int = 0 

class UserJSON(BaseModel):
    username: str
    admin: int = 0

class Player(BaseModel):
    id: int
    name: str | None = None
    number: int | None
    pos: str

class PlayerStat(BaseModel):
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

class Games(BaseModel):
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