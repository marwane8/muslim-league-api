#from app.accessors.bball.bball_accessor import *
from app.processors.soccer import  *
from app.accessors.soccer import *


#data comment
stat1 = SoccerStat(
    game_id=1,
    player_id=1,
    goals=2,
    assists=3
)

stat2 = SoccerStat(
    game_id=3,
    player_id=1,
    goals=2,
    assists=3
)
stat3 = SoccerStat(
    game_id=1,
    player_id=1,
    goals=2,
    assists=2
)


stats = [stat1,stat2,stat3]
data = insert_soccer_stats(stats)
print(data)
