import os
from fastapi import FastAPI, Depends,Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.auth_deps import get_current_user,badLoginException
from app.models.user_models import User,TokenSchema

from app import sport_rt

from app.utils.auth_utils import ( 
    create_access_token,
    verify_password,
    get_credentials_from_db
)


app = FastAPI()
app_env = os.environ.get('ML_ENV') 

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

#Included routers
app.include_router(sport_rt.router)

@app.get("/api")
def home():
    return  { "message": "The Muslim League API"}


#--------------
# User Authentication Endpoints
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
