from app.processors.soccer import *

standings = get_stat_leaders(Stat.GOALS,1)
print(standings)