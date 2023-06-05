from pydantic import BaseModel 

class Team(BaseModel):
    team_id: int
    season_id: int
    team_name: str
    team_captain: str 
    wins: int
    losses: int
    goals_for: int
    goals_against: int
    points: int