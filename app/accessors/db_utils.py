import os
import sqlite3
from enum import Enum
from passlib.context import CryptContext
from app.user_models import User


USERS_DB_URL = os.environ.get('USERS_DB_URL') 
BBALL_DB_URL = os.environ.get('BBALL_DB_URL') 
SOCCER_DB_URL = os.environ.get('SOCCER_DB_URL') 

class DB(Enum):
    USERS = 1
    BBALL = 2
    SOCCER = 3

def get_db_url(database: DB) -> str:
    databases = {
        DB.USERS: USERS_DB_URL,
        DB.BBALL: BBALL_DB_URL,
        DB.SOCCER: SOCCER_DB_URL
    }
    return databases.get(database,None)
     
# Password Hashing Utilities
password_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def get_credentials_from_db(username: str) -> User | None:

    query = "SELECT username,admin,password FROM Users WHERE username = ?"
    record = fetchone_sql_statement(query,(username,))
    if not record: 
        print("The User Not Found: ", username)
        return None 
    user = User( username=record[0], admin=record[1], password=record[2])
    return user


# DB Access Utilities
def fetchone_sql_statement(database: DB,query,values) -> list:
    db_url = get_db_url(database)
    print(db_url)
    try:
        connection = sqlite3.connect(db_url)
        cursor = connection.cursor()
        cursor.execute(query,values)

        log_message = 'Executing Statement: {} with values {}'.format(query,values)
        print(log_message)

        record = cursor.fetchone()
        return record
    except sqlite3.Error as error:
        print('DB Request Failed: {}'.format(error))
    finally:
        if connection:
            connection.close()
            print("Closing SQLite Connection")


def execute_sql_statement(database: DB,query,values=None) -> list:
    db_url = get_db_url(database)
    try:
        connection = sqlite3.connect(db_url)
        cursor = connection.cursor()
        if values: 
            cursor.execute(query,values)
        else:
            cursor.execute(query)

        log_message = 'Executing Statement: {} with | values {}'.format(query,values)
        print(log_message)

        record = cursor.fetchall()
        return record
    except sqlite3.Error as error:
        print('DB Request Failed: {}'.format(error))
    finally:
        if connection:
            connection.close()
            print("Closing SQLite Connection")

def commit_sql_statement(database: DB,query,values) -> list:

    db_url = get_db_url(database)
    try:
        connection = sqlite3.connect(db_url)
        cursor = connection.cursor()

        log_message = 'Executing Statement: {} with | values {}'.format(query,values)
        print(log_message)
        cursor.execute(query,values)
        record = cursor.fetchall()
        connection.commit()
        return record
    except sqlite3.Error as error:
        print('DB Request Failed: {}'.format(error))
    finally:
        if connection:
            connection.close()
            print("Closing SQLite Connection")

def execute_bulk_insert(database: DB,query,values: list[tuple]) -> list:
    db_url = get_db_url(database)
    try:
        connection = sqlite3.connect(db_url)
        connection.execute("PRAGMA foreign_keys = ON") 
        cursor = connection.cursor()

        for value in values:
            cursor.execute(query,value)

        log_message = 'Updating query: {} with | number of values {}'.format(query,len(values))
        print(log_message)
        connection.commit()
    except sqlite3.Error as error:
        raise RuntimeError('SQL error inserting data: {}'.format(error))
    finally:
        if connection:
            connection.close()
            print("Closing SQLite Connection")

