from app.auth_deps import get_current_user,badLoginException
from fastapi import FastAPI, Path, Depends,Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

from app.models import Player,Team, User, TokenSchema 
from app.utils import ( 
    create_access_token,
    verify_password,
    get_credentials_from_db
)

from app.db_accessor import (
    get_team_standings,
    get_team_roster
)


app_env = os.environ.get('ML_ENV') 

app = FastAPI()
app_domain = "localhost"

if app_env == 'prod':
    app = FastAPI(docs_url=None,redoc_url=None)
    app_domain = ".muslimleaguect.com"

origins = [
  "http://localhost:3000",
  "https://www.muslimleaguect.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
def home():
    return  { "message": "The Muslim League API"}


#--------------
# User Authenticatoin Endpoints
#--------------
@app.post("/api/v1/login",summary="Verifies user and returns jwt token", response_model=TokenSchema)
def login(response: Response,form_data: OAuth2PasswordRequestForm = Depends()):

    input_username = form_data.username  
    input_password = form_data.password 

    user_info = get_credentials_from_db(input_username)   
    if user_info: is_valid_password = verify_password(input_password,user_info.password)

    if not user_info or not is_valid_password:
        raise badLoginException
    
    jwtToken = create_access_token(user_info.username,admin=user_info.admin)

    response.set_cookie(key="token", value=jwtToken,secure=True,domain=app_domain)

    token_json = {
        "access_token": jwtToken
    }

    return token_json 


@app.get("/api/v1/logout",summary="Logs out user and clears cookies")    
def logout(user: User = Depends(get_current_user)):
    message = {"message" : "Logout Success"}
    response = JSONResponse(content=message) 
    response.set_cookie(key="token", value="",secure=True,domain=app_domain)
    return response

#--------------
# TEAM API Endpoints
#--------------
get_standings_summary = "Returns a sorted list of teams of a given season id according their prefomance records"
@app.get("/api/v1/teams/standings/{season_id}" ,summary=get_standings_summary, response_model=list[Team])
def get_standings(season_id: int = Path(None,description="The ID of a Season")):
    standings = get_team_standings(season_id)
    return standings 

get_roster_summary = "Returns a list of players associated with the given team id"
@app.get("/api/v1/teams/{team_id}" ,summary=get_roster_summary, response_model=list[Player])
def get_roster(team_id: int = Path(None,description="The ID of a Team")):
    roster = get_team_roster(team_id)
    return roster 