from ..models.bball_models import Team,GameStats


def map_row_to_team(record: list) -> list[Team]:
        teams = []
        if record == []:
            print("No records found for requested team")
        else:
            for team_info in record:
                (id, name, wins, loss, points_for, 
                 points_against, rebounds_total) = team_info

                teams.append(Team(id=id,name=name,wins=wins,loss=loss,
                            points_for=points_for,points_against=points_against,
                            rebounds_total=rebounds_total))
        return teams 


def map_row_to_game_stats(records: list[tuple]) -> list[GameStats]:
    game_stats = []
    if records == []:
        print("Not teams found for requested season")
    else:
        for game_data in records:
            g_id,t_id,team_name,total_pts,total_reb,fls = game_data[:6] 
            game = GameStats(
                 game_id=g_id,
                 team_id=t_id,
                 team_name=team_name,
                 points=total_pts,
                 rebounds=total_reb,
                 fouls=fls
            )
            game_stats.append(game)

    return game_stats

