from ..models.sport_models import *

def map_rows_to_seasons(rows) -> list[Season]:
    seasons = []
    for row in rows:
        season_id,season_name,year = row
        season = Season(
             season_id=season_id,
             season_name=season_name,
             year=year
        )
        seasons.append(season)
    return seasons

def map_rows_to_players(rows) -> list[Player]:
    players = []
    for row in rows:
        player_id,team_id,team_name,player_name,player_number,player_pos  = row
        player = Player(
            player_id=player_id,
            team_id=team_id,
            team_name=team_name,
            player_name=player_name,
            player_number=player_number,
            player_pos=player_pos
        )
        players.append(player)
    return players

def map_row_to_games(rows) -> list[Game]:
        games = []
        for row in rows:
                season_id,game_id,team1_id,team1,team2_id,team2,date,start_time,court,playoff = row
                game = Game(
                    season_id=season_id,
                    game_id=game_id,
                    team1_id=team1_id,
                    team1=team1,
                    team2_id=team2_id,
                    team2=team2,
                    date=date,
                    start_time=start_time,
                    court=court,
                    playoff=playoff
                )
                games.append(game)
        return games 

def map_row_to_stat(record: list) -> list[PlayerStat]:
        roster = []
        if record == []:
            print("No records found for requested team")
        else:
            for player_stat in record:
                p_id,p_name,p_games,p_stat = player_stat
                roster.append(PlayerStat(id=p_id,name=p_name,games=p_games,stat=p_stat))
        return roster

