from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.models import TokenPayload, User
from app.utils import ALGORITHM,JWT_SECRET_KEY,get_credentials_from_db

from jose import jwt
from pydantic import ValidationError

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/v1/login",
    scheme_name="JWT"
) 

def get_current_user(token: str = Depends(reuseable_oauth)) -> User:
    try:
        payload = jwt.decode( token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data =  TokenPayload(**payload)

        isTokenExpired = datetime.fromtimestamp(token_data.exp) < datetime.now()
        if isTokenExpired:
            raise tokenExpiredException 
    
    except(jwt.JWTError, ValidationError):
        raise forbiddenException

    username = token_data.sub
    user = get_credentials_from_db(username)
    user.password = None

    if user is None:
        raise notFoundException    

    return user

tokenExpiredException: HTTPException = HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Token expired",
            headers={"WWW-Authenticate": "Bearer"}
        )

forbiddenException: HTTPException = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

notFoundException: HTTPException = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user"
        )

badLoginException: HTTPException = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
