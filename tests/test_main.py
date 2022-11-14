import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_read_main(client):
    # ARRANGE
    response = client.get("/")
    
    #ASSERT
    assert response.status_code == 200
    assert response.json() == {"message":"Muslim League API"}

def test_login_failure(client):    
    #ARRANGE
    testFormData = { 
        "username": "user",
        "password": "password",
        "grant_type": "password"
    }
    testHeaders = {
        "content-type":"application/x-www-form-urlencoded"
    }
    
    response = client.post("/login", data=testFormData,
                            headers=testHeaders)

    assert response.status_code == 401 
    assert response.cookies.get("token") == None
