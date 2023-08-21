from ..models.bball_models import Team,GameStats


def map_row_to_team(record: list) -> list[Team]:
        teams = []
        if record == []:
            print("No records found for requested team")
        else:
            for team_info in record:
                t_id,t_name = team_info
                teams.append(Team(id=t_id,name=t_name))
        return teams 

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

