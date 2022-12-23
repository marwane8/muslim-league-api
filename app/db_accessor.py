from app.models import Player 
from app.models import Team,TeamStats,PlayerStats,GameDates,Game,GameStats
from app.utils import execute_sql_statement
# DB Constants

#--------------
# Teams Functions 
#--------------
def get_all_teams(season_id: int) -> list[Team]:
    teams_query = "SELECT team_id,team_name FROM Teams WHERE season_id=?"
    teams_records = execute_sql_statement(teams_query,(season_id,))
    teams = map_row_to_team(teams_records) 
    return teams

def get_team_standings(season_id: int) -> list[TeamStats]:
    teams_query = "SELECT team_id,team_name,wins,losses,PF,PA,rebounds_tot FROM Teams WHERE season_id=?"
    teams_records = execute_sql_statement(teams_query,(season_id,))
    standings = map_teams_to_standings(teams_records) 
    return standings

#--------------
# Players Functions 
#--------------
def get_team_roster(team_id: int) -> list[Player]:

    roster_query = "SELECT id,player_name,player_number,player_pos FROM roster WHERE team_id = ?"
    roster_records = execute_sql_statement(roster_query,(team_id,))
    roster = map_row_to_player(roster_records)
    return roster

def get_points_leaders(season_id: int=None) -> list[PlayerStats]:
    #TODO: Implement Season Filter in DB
    point_stat_query = "SELECT p_id,name,games_played,points FROM player_totals"
    point_stat_records = execute_sql_statement(point_stat_query)
    points_leaders = map_stat_to_leaders(point_stat_records) 

    return points_leaders 

def get_rebound_leaders(season_id: int=None) -> list[PlayerStats]:
    #TODO: Implement Season Filter in DB
    point_stat_query = "SELECT p_id,name,games_played,rebounds FROM player_totals"
    point_stat_records = execute_sql_statement(point_stat_query)
    rebound_leaders= map_stat_to_leaders(point_stat_records) 
    return rebound_leaders

#--------------
# Games Functions 
#--------------
def get_game_days() -> GameDates:
    game_day_query = "SELECT date FROM Games GROUP BY date"
    game_days_records= execute_sql_statement(game_day_query)
    game_days = map_date_record(game_days_records)
    return game_days

def get_games_of_date(date: int) -> list[Game]:
    game_query= "SELECT game_id,team1_id,team1,team2_id,team2,date,start_time,court,playoff FROM schedule WHERE date = ?"
    games_records = execute_sql_statement(game_query,(date,))
    games = map_row_to_games(games_records)
    return games

def get_games_stats(game_id: int) -> list[GameStats]:
    game_stats_query= "SELECT g_id,t_id,team_name,total_pts,total_reb,fls FROM game_totals WHERE g_id = ?"
    games_records = execute_sql_statement(game_stats_query,(game_id,))
    games = map_game_stats(games_records)
    return games
 
 

#--------------
# Mapping Functions 
#--------------
def map_row_to_team(record: list) -> list[Team]:
        teams = []
        if record == []:
            print("No records found for requested team")
        else:
            for team_info in record:
                t_id,t_name = team_info
                teams.append(Team(id=t_id,name=t_name))
        return teams 

def map_teams_to_standings(records: list) -> list[TeamStats]:
    standings = []
    if records == []:
        print("Not teams found for requested season")
    else:
        for team_data in records:
            diff = team_data[4] - team_data[5]
            id,name,w,l,pf,pa,rebs = team_data[0:7] 
            team = TeamStats(id=id,name=name,wins=w,loss=l,points_for=pf,points_against=pa,rebounds_total=rebs,diff=diff)
            standings.append(team)
        standings.sort(key=lambda t: (-t.wins, -t.diff))
    return standings

def map_row_to_player(record: list) -> list[Player]:
        roster = []
        if record == []:
            print("No records found for requested team")
        else:
            for player_info in record:
                p_id,p_name,p_num,p_pos = player_info
                roster.append(Player(id=p_id,name=p_name,number=p_num,pos=p_pos))
        return roster

def map_row_to_games(record: list) -> list[Game]:
        games = []
        if record == []:
            print("No records found for requested team")
        else:
            for game_info in record:
                g_id,t1_id,tm1,t2_id,tm2,date,start_time,court,playoff = game_info
                games.append(Game(game_id=g_id,team1_id=t1_id,team1=tm1,team2_id=t2_id,team2=tm2,date=date,start_time=start_time,court=court,playoff=playoff))
        return games 


def map_stat_to_leaders(records: list) -> list[PlayerStats]:
    leaders = []
    if records == []:
        print("Not teams found for requested season")
    else:
        for stat_data in records:
            stat_average = "{:.1f}".format(stat_data[3]/stat_data[2])
            p_id,p_name = stat_data[:2] 
            player = PlayerStats(id=p_id,name=p_name,stat=stat_average)
            leaders.append(player)
    leaders.sort(key=lambda p: float(p.stat),reverse=True)
    return leaders[:5] 

def map_date_record(records: list[tuple]) -> GameDates:
    dates = []
    if records == []:
        print("Not teams found for requested season")
    dates = [ date[0] for date in records]
    game_dates=GameDates(games=dates)
    return game_dates 

def map_game_stats(records: list[tuple]) -> list[GameStats]:
    game_stats = []
    if records == []:
        print("Not teams found for requested season")
    else:
        for game_data in records:
            g_id,t_id,team_name,total_pts,total_reb,fls = game_data[:6] 
            game = GameStats(game_id=g_id,team_id=t_id,team_name=team_name,points=total_pts,rebounds=total_reb,fouls=fls)
            game_stats.append(game)

    return game_stats

