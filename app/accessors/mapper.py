import json
from ..models.sport_models import *

def map_rows_to_seasons(rows) -> list[Season]:
    seasons = []
    for row in rows:
        id,sport_id,name,year = row
        season = Season(
             id=id,
             sport_id=sport_id,
             name=name,
             year=year
        )
        seasons.append(season)
    return seasons

def map_row_to_team(record: list) -> list[TeamData]:
        teams = []
        if record == []:
            print("No records found for requested team")
        else:
            for team_info in record:
                (id, season_id, name, captain_id, stats_obj) = team_info
                stats_dict = {}
                if stats_obj:
                     stats_dict = json.loads(stats_obj)
                teams.append(TeamData(
                    id=id,
                    season_id=season_id,
                    name=name,
                    captain_id=captain_id,
                    stats_obj=stats_dict
                ))

        return teams 


def map_rows_to_players(rows) -> list[Player]:
    players = []
    for row in rows:
        player_id,team_id,team_name,active,f_name,l_name,player_name,player_number,player_pos  = row
        player = Player(
            player_id=player_id,
            team_id=team_id,
            team_name=team_name,
            active=active,
            f_name=f_name,
            l_name=l_name,
            name=player_name,
            number=player_number,
            pos=player_pos
        )
        players.append(player)
    return players

def map_row_to_games(rows) -> list[Game]:
        games = []
        for row in rows:
                sport_id, season_id,game_id,team1_id,team1,team2_id,team2,date,start_time,court,playoff,played = row
                game = Game(
                    sport_id=sport_id,
                    season_id=season_id,
                    game_id=game_id,
                    team1_id=team1_id,
                    team1=team1,
                    team2_id=team2_id,
                    team2=team2,
                    date=date,
                    start_time=start_time,
                    court=court,
                    playoff=playoff,
                    played=played
                )
                games.append(game)
        return games 


def map_row_to_stat(record: list,category) -> list[PlayerStat]:
        player = []
        if record == []:
            print("No records found for requested team")
        else:
            for player_stat in record:
                season_id, player_id, name, stat_records, dnp, type, stat = player_stat
                stat = PlayerStat(
                    season_id=season_id,
                    player_id=player_id,
                    name=name,
                    stat_records=stat_records,
                    dnp=dnp,
                    type=category,
                    stat=stat
                )
                player.append(stat)
        return player 


def map_row_to_player_game_stats(records:  list[tuple], stat_lookup) -> list[PlayerGameStats]:
    player_game_stats = []

    for game_stat in records:

        game_id, team_id, team_name, player_id, stat_id, player_name, type1, stat1, type2, stat2, type3, stat3 = game_stat
        stat = PlayerGameStats(
            game_id=game_id,
            team_id=team_id,
            team_name=team_name,
            player_id=player_id,
            stat_id=stat_id,
            player_name=player_name,
            type1=stat_lookup[type1],
            stat1=stat1,
            type2=stat_lookup[type2],
            stat2=stat2,
            type3=stat_lookup[type3],
            stat3 =stat3
        )

        player_game_stats.append(stat)
    
    return player_game_stats


def map_row_to_game_totals(games_records,stat_lookup) -> [TeamGameStats]:
    game_totals = []
    for row in games_records:
            t_id, team_name, g_id, type1, stat1_total, type2, stat2_total, type3, stat3_total = row

            stats = TeamGameStats(
                t_id=t_id,
                team_name=team_name,
                g_id=g_id,
                type1=stat_lookup[type1],
                stat1_total=stat1_total,
                type2=stat_lookup[type2],
                stat2_total=stat2_total,
                type3=stat_lookup[type3],
                stat3_total=stat3_total
            )

            game_totals.append(stats)
    return game_totals 
