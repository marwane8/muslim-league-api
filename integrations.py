#from app.accessors.bball.bball_accessor import *
from app.processors.soccer import  *

data = get_stat_leaders(Stat.ASSISTS,2)
print(data)
