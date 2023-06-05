from pydantic import BaseModel 

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

class Player(BaseModel):
    player_id: int 
    team_id: int 
    team_name: str 
    player_name: str 
    player_number: str 
    player_pos: str

class PlayerTotals(BaseModel):
    player_id: int
    player_name: str
    games_played: int 
    goals: int
    assists: int