from .bball_mapper import *
from .bball_models import Player,PlayerStats,Team,TeamStats,GameDates,Game,GameStats,Season
from ..db_utils import DB,execute_sql_statement,fetchone_sql_statement,commit_sql_statement

#--------------
# Seasons  
#--------------
def get_seasons_data() -> list[Season]:
    teams_query = "SELECT season_id, season_name, year FROM seasons"
    teams_records = execute_sql_statement(DB.SOCCER,teams_query)
    teams = map_rows_to_seasons(teams_records) 
    return teams


#--------------
# Teams Functions 
#--------------
def get_all_teams(season_id: int) -> list[Team]:
    teams_query = "SELECT team_id,team_name FROM Teams WHERE season_id=?"
    teams_records = execute_sql_statement(DB.BBALL,teams_query,(season_id,))
    teams = map_row_to_team(teams_records) 
    return teams

def get_team_standings(season_id: int) -> list[TeamStats]:
    teams_query = "SELECT team_id,team_name,wins,losses,PF,PA,rebounds_tot FROM Teams WHERE season_id=?"
    teams_records = execute_sql_statement(DB.BBALL,teams_query,(season_id,))
    standings = map_teams_to_standings(teams_records) 
    return standings

#--------------
# Players Functions 
#--------------
def get_team_roster(team_id: int) -> list[Player]:

    roster_query = "SELECT id,player_name,player_number,player_pos FROM roster WHERE team_id = ?"
    roster_records = execute_sql_statement(DB.BBALL,roster_query,(team_id,))
    roster = map_row_to_player(roster_records)
    return roster

def get_points_leaders(season_id: int=None) -> list[PlayerStats]:
    #TODO: Implement Season Filter in DB
    point_stat_query = "SELECT p_id,name,games_played,points FROM player_totals"
    point_stat_records = execute_sql_statement(DB.BBALL,point_stat_query)
    points_leaders = map_stat_to_leaders(point_stat_records) 

    return points_leaders 

def get_rebound_leaders(season_id: int=None) -> list[PlayerStats]:
    #TODO: Implement Season Filter in DB
    point_stat_query = "SELECT p_id,name,games_played,rebounds FROM player_totals"
    point_stat_records = execute_sql_statement(DB.BBALL,point_stat_query)
    rebound_leaders= map_stat_to_leaders(point_stat_records) 
    return rebound_leaders

#--------------
# Games Functions 
#--------------
def get_game_days() -> GameDates:
    game_day_query = "SELECT date FROM Games GROUP BY date"
    game_days_records= execute_sql_statement(DB.BBALL,game_day_query)
    game_days = map_date_record(game_days_records)
    return game_days

def get_games_of_date(date: int) -> list[Game]:
    game_query= "SELECT game_id,team1_id,team1,team2_id,team2,date,start_time,court,playoff FROM schedule WHERE date = ?"
    games_records = execute_sql_statement(DB.BBALL,game_query,(date,))
    games = map_row_to_games(games_records)
    return games

def get_games_stats(game_id: int) -> list[GameStats]:
    game_stats_query= "SELECT g_id,t_id,team_name,total_pts,total_reb,fls FROM game_totals WHERE g_id = ?"
    games_records = execute_sql_statement(DB.BBALL,game_stats_query,(game_id,))
    games = map_game_stats(games_records)
    return games

#--------------
# Stat Calculation Functions
#--------------
def update_team_stats(team_id: int):
    points_for,points_against,rebound_totals,foul_totals = get_team_stats(team_id)
    update_query =  "UPDATE teams SET PF=?,PA=?,rebounds_tot=?,fouls_tot=? WHERE team_id=?"
    commit_sql_statement(DB.BBALL,update_query,(points_for,points_against,rebound_totals,foul_totals,team_id))

def get_team_stats(team_id: int) -> tuple:
    games=get_games_played(team_id)
    point_stats=calc_team_scoring_stats(team_id,games)
    wins,losses,ties,points_for,points_against = point_stats
    get_stat_record_query = "SELECT total_reb,fls FROM team_totals WHERE t_id = ?"
    rebound_totals,foul_totals= fetchone_sql_statement(DB.BBALL,get_stat_record_query,(team_id,)) 
    return (points_for,points_against,rebound_totals,foul_totals)

def get_games_played(team_id: int) -> list[int]:
    games_played_query = "SELECT g_id FROM game_totals WHERE t_id=?;"
    game_records = execute_sql_statement(DB.BBALL,games_played_query,(team_id,))
    game_ids = [ game[0] for game in game_records]
    print(game_ids)
    return game_ids

def calc_team_scoring_stats(team_id: int, game_ids: tuple[int]):
    wins,losses,draws=0,0,0
    points_for,points_against = 0,0
    get_game_result_query = "SELECT t_id,total_pts FROM game_totals WHERE g_id=?" 
    for game_id in game_ids:
        home_record,away_record=execute_sql_statement(DB.BBALL,get_game_result_query,(game_id,))
        if home_record[0] == team_id:
            team_points = home_record[1]
            opp_points = away_record[1]
        else:
            team_points = away_record[1]
            opp_points = home_record[1]

        if team_points > opp_points: 
            wins += 1
        elif team_points == opp_points:
            draws += 1
        else: 
            losses += 1
        
        points_for += team_points
        points_against += opp_points
    return (wins,losses,draws,points_for,points_against)
        
