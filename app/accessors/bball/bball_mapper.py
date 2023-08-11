from .bball_models import Player,PlayerStats,Team,TeamStats,GameDates,Game,GameStats,Season

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

def map_row_to_stat(record: list) -> list[PlayerStats]:
        roster = []
        if record == []:
            print("No records found for requested team")
        else:
            for player_stat in record:
                p_id,p_name,p_games,p_stat = player_stat
                roster.append(PlayerStats(id=p_id,name=p_name,games=p_games,stat=p_stat))
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

