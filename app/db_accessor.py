from app.models import Player 
from app.models import Team 
from app.utils import execute_sql_statement
# DB Constants

def get_team_roster(team_id: int) -> list[Player]:

    roster_query = "SELECT id,player_name,player_number,player_pos FROM roster WHERE team_id = ?"
    roster_records = execute_sql_statement(roster_query,(team_id,))
    roster = map_row_to_player(roster_records)
    return roster

def get_team_standings(season_id: int) -> list[Team]:

    teams_query = "SELECT team_id,team_name,wins,losses,PF,PA FROM Teams WHERE season_id=?"
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
            team_id,team_name,w,l = team_data[0:4] 
            team = Team(id=team_id,name=team_name,wins=w,loss=l,diff=diff)
            standings.append(team)
            standings.sort(key=lambda t: (-t.wins, -t.diff))
    return standings

     
 