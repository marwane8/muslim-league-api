
from app.accessors.db_accessor import Accessor 
from app.models.bball_models import *
from app.models.sport_models import *


class Processor():
    def __init__(self):
        self.db_accessor = Accessor()
    
    def get_seasons(self):
        return self.db_accessor.get_seasons_data()
