#from app.accessors.bball.bball_accessor import *
from app.processors.soccer import  *
from app.accessors.soccer import *

from app.utils import auth_utils

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
passw = auth_utils.get_hashed_password('Bismillah114');
print(passw)