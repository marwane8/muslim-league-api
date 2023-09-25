import os
import sqlite3
from enum import Enum
from passlib.context import CryptContext
from app.models.user_models import User

DB_URL = os.environ.get('DB_URL') 
     
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
def fetchone_sql_statement(query,values) -> list:
    try:
        connection = sqlite3.connect(DB_URL)
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


def execute_sql_statement(query,values=None) -> list:
    try:
        connection = sqlite3.connect(DB_URL)
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

def commit_sql_statement(query,values) -> list:
    try:
        connection = sqlite3.connect(DB_URL)
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

def execute_bulk_query(query,values: list[tuple]) -> list:
    try:
        connection = sqlite3.connect(DB_URL)
        connection.execute("PRAGMA foreign_keys = ON") 
        cursor = connection.cursor()

        for value in values:
            cursor.execute(query,value)

        log_message = f'Insert Success - {len(values)} row inserted'
        print(log_message)
        connection.commit()
    except sqlite3.Error as error:
        raise RuntimeError('error inserting data - {}'.format(error))
    finally:
        if connection:
            connection.close()
            print("Closing SQLite Connection")

def insert_many_to_many_query(connection,main_query,values,ref_query,refID):
        connection.execute("PRAGMA foreign_keys = OFF") 
        cursor = connection.cursor()
        cursor.execute(main_query,values)
        cursor.execute("SELECT last_insert_rowid()")
        record = cursor.fetchone()
        lastID = record[0]
        ref_values = (refID,lastID)
        cursor.execute(ref_query,ref_values)
