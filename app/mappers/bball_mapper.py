from ..models.bball_models import BBallTeamData,GameStats, PlayerGameStats


def map_row_to_team(record: list) -> list[BBallTeamData]:
        teams = []
        if record == []:
            print("No records found for requested team")
        else:
            for team_info in record:
                (id, season_id, name, captain, wins, loss, points_for, 
                 points_against, rebounds_total) = team_info

                teams.append(BBallTeamData(
                    team_id=id,
                    season_id=season_id,
                    team_name=name,
                    team_captain=captain,
                    wins=wins,
                    loss=loss,
                    points_for=points_for,
                    points_against=points_against,
                    rebounds_total=rebounds_total
                ))

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



def map_row_to_player_game_stats(records:  list[tuple]) -> list[PlayerGameStats]:
    player_game_stats = []

    for game_stat in records:
        game_id, team_id, team_name, player_id, stat_id, player_name, dnp, points, rebounds, fouls = game_stat
        stat = PlayerGameStats(
            game_id=game_id,
            team_id=team_id,
            team_name=team_name,
            player_id=player_id,
            stat_id=stat_id,
            player_name=player_name,
            dnp=dnp,
            points=points,
            rebounds=rebounds,
            fouls=fouls
        )

        player_game_stats.append(stat)
    
    return player_game_stats