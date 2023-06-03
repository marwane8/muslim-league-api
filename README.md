# Muslim League API
Main backend api for muslim league app. 

To build project
1. Create virtual environment:  
    `python3 -m venv .venv`

2. Activate Virtual Environment:    
    `source .venv/bin/activate`

3. Install dependencies:    
    `python3 -m pip install -r requirements.txt`

4. Set Environment variable in `.venv/bin/activate` script:    
    `USERS_DB_URL=<path-to-db>`
    `BBALL_URL=<path-to-db>`
    `SOCCER_DB_URL=<path-to-db>`

To run application in development:
    `uvicorn app.main:app --reload`
