from typing import Any
from datetime import datetime, timedelta

import os
from jose import jwt
from passlib.context import CryptContext


from app.user_models import User
from .accessors.db_utils import DB,fetchone_sql_statement

ENVIRONMENT = os.environ.get('ML_ENV') 

# JWT Constants
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"

JWT_SECRET_KEY = "key1" 
if ENVIRONMENT=="prod":
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') 


# JWT Creation Utilities
def create_access_token(subject: str | Any, admin: int, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject),"admin": bool(admin)}
    encoded_jwt = jwt.encode(to_encode,JWT_SECRET_KEY,ALGORITHM)
    return encoded_jwt

# Password Hashing Utilities
password_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def get_credentials_from_db(username: str) -> User | None:

    query = "SELECT username,admin,password FROM Users WHERE username = ?"
    record = fetchone_sql_statement(DB.USERS,query,(username,))
    if not record: 
        print("The User Not Found: ", username)
        return None 
    user = User( username=record[0], admin=record[1], password=record[2])
    return user

