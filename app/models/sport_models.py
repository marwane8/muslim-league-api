from pydantic import BaseModel 

class Season(BaseModel):
    id: int
    sport_id: int
    name: str
    year: int

class TeamData(BaseModel):
    id: int
    season_id: int
    name: str | None = None
    captian_id: str | None = None
    stats_obj: dict 

class BballStandings(BaseModel):
    id: int
    season_id: int
    name: str | None = None
    wins: int
    losses: int
    points_for: int
    points_against: int
    rebounds: int
    fouls: int


class Player(BaseModel):
    player_id: int | None
    team_id: int 
    team_name: str 
    active: int
    f_name: str 
    l_name: str 
    name: str 
    number: str 
    pos: str

class Game(BaseModel):
    sport_id: int
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
    played: int

class PlayerStat(BaseModel):
    season_id: int
    player_id: int
    name: str | None = ''
    stat_records: int
    dnp: int
    type: str 
    stat: int 


class TeamGameStats(BaseModel):
    t_id : int
    team_name : str
    g_id : int
    type1 : str
    stat1_total : int
    type2 : str
    stat2_total : int
    type3 : str
    stat3_total  : int


class PlayerGameStats(BaseModel):
    game_id : int
    team_id : int
    team_name : str
    player_id : int
    stat_id : int
    player_name : str
    type1 : str
    stat1 : int
    type2 : str
    stat2 : int
    type3 : str
    stat3  : int

class StatUpsert(BaseModel):
    id: int | None
    sport_id: int
    game_id: int
    player_id: int
    dnp: int
    stat1_type: int
    stat1: int
    stat2_type: int
    stat2: int
    stat3_type: int
    stat3: int




