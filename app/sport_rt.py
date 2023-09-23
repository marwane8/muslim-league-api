from fastapi import APIRouter,Path,Depends,HTTPException

from app.auth_deps import get_current_user

from .models.user_models import User
from .models.sport_models import *

from .processors.processor import Processor


router = APIRouter(
    prefix="/api/v1",
    tags=["sport"]
)

proc = Processor()
#--------------
# Season API Endpoints
#--------------
get_teams_summary= "Returns a list of all available seasons"
@router.get("/seasons" ,summary=get_teams_summary, response_model=list[Season])
def get_all_seasons():
    return proc.get_seasons()

