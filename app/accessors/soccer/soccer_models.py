from pydantic import BaseModel 

class Season(BaseModel):
    season_id: int
    season_name: str
    year: int

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

class GameDates(BaseModel):
    games: list[int]

class GameStats(BaseModel):
    game_id: int
    team_id: int
    team_name: str
    goals: int
    assists: int