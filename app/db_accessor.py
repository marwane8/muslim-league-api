from app.models import Player 
from app.models import Team 
from app.utils import execute_sql_statement,fetchone_sql_statement,commit_sql_statement
# DB Constants

def get_team_roster(team_id: int) -> list[Player]:

    roster_query = "SELECT id,player_name,player_number,player_pos FROM roster WHERE team_id = ?"
    roster_records = execute_sql_statement(roster_query,(team_id,))
    roster = map_row_to_player(roster_records)
    return roster

def get_team_standings(season_id: int) -> list[Team]:
    teams_query = "SELECT team_id,team_name,wins,losses,PF,PA,rebounds_tot FROM Teams WHERE season_id=?"
    teams_records = execute_sql_statement(teams_query,(season_id,))
    standings = map_teams_to_standings(teams_records) 
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


def map_teams_to_standings(records: list) -> list[Team]:
    standings = []
    if records == []:
        print("Not teams found for requested season")
    else:
        for team_data in records:
            diff = team_data[4] - team_data[5]
            id,name,w,l,pf,pa,rebs = team_data[0:7] 
            team = Team(id=id,name=name,wins=w,loss=l,points_for=pf,points_against=pa,rebounds_total=rebs,diff=diff)
            standings.append(team)
            standings.sort(key=lambda t: (-t.wins, -t.diff))
    return standings


def update_team_stats(team_id: int):
    points_for,points_against,rebound_totals,foul_totals = get_team_statistics(team_id)
    update_query =  "UPDATE teams SET PF=?,PA=?,rebounds_tot=?,fouls_tot=? WHERE team_id=?"
    commit_sql_statement(update_query,(points_for,points_against,rebound_totals,foul_totals,team_id))


def get_team_statistics(team_id: int) -> list:
    games=get_games_played(team_id)
    point_stats=calc_team_scoring_stats(team_id,games)
    wins,losses,ties,points_for,points_against = point_stats
    get_stat_record_query = "SELECT total_reb,fls FROM team_totals WHERE t_id = ?"
    rebound_totals,foul_totals= fetchone_sql_statement(get_stat_record_query,(team_id,)) 
    return (points_for,points_against,rebound_totals,foul_totals)

def calc_team_scoring_stats(team_id: int, game_ids: tuple[int]):
    wins,losses,draws=0,0,0
    points_for,points_against = 0,0
    get_game_result_query = "SELECT t_id,total_pts FROM game_totals WHERE g_id=?" 
    for game_id in game_ids:
        home_record,away_record=execute_sql_statement(get_game_result_query,(game_id,))
        if home_record[0] == team_id:
            team_points = home_record[1]
            opp_points = away_record[1]
        else:
            team_points = away_record[1]
            opp_points = home_record[1]

        if team_points > opp_points: 
            print('game: ' + str(game_id) + ' team wins')
            wins += 1
        elif team_points == opp_points:
            draws += 1
        else: 
            print('game: ' + str(game_id) + ' team losses')
            losses += 1
        
        points_for += team_points
        points_against += opp_points

    return (wins,losses,draws,points_for,points_against)
        
def get_games_played(team_id: int) -> list[int]:
    games_played_query = "SELECT g_id FROM game_totals WHERE t_id=?;"
    game_records = execute_sql_statement(games_played_query,(team_id,))
    game_ids = [ game[0] for game in game_records]
    print(game_ids)
    return game_ids

get_team_standings(3)