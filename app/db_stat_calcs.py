from app.utils import execute_sql_statement,fetchone_sql_statement,commit_sql_statement

#--------------
# Stat Calculation Functions
#--------------
def update_team_stats(team_id: int):
    points_for,points_against,rebound_totals,foul_totals = get_team_stats(team_id)
    update_query =  "UPDATE teams SET PF=?,PA=?,rebounds_tot=?,fouls_tot=? WHERE team_id=?"
    commit_sql_statement(update_query,(points_for,points_against,rebound_totals,foul_totals,team_id))

def get_team_stats(team_id: int) -> tuple:
    games=get_games_played(team_id)
    point_stats=calc_team_scoring_stats(team_id,games)
    wins,losses,ties,points_for,points_against = point_stats
    get_stat_record_query = "SELECT total_reb,fls FROM team_totals WHERE t_id = ?"
    rebound_totals,foul_totals= fetchone_sql_statement(get_stat_record_query,(team_id,)) 
    return (points_for,points_against,rebound_totals,foul_totals)

def get_games_played(team_id: int) -> list[int]:
    games_played_query = "SELECT g_id FROM game_totals WHERE t_id=?;"
    game_records = execute_sql_statement(games_played_query,(team_id,))
    game_ids = [ game[0] for game in game_records]
    print(game_ids)
    return game_ids

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
            wins += 1
        elif team_points == opp_points:
            draws += 1
        else: 
            losses += 1
        
        points_for += team_points
        points_against += opp_points
    return (wins,losses,draws,points_for,points_against)
        
