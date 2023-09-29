import pytest
from app.utils import auth_utils

def test_verify_password():
    
    #hash for word "pass"
    hashed_pass= "$2b$12$3vjRF4p3SIRF5TfpnoxkYuxJD2ACsXlGhWm4MO5N96pPuL.FlFDd2"

    assert auth_utils.verify_password('pass',hashed_pass) == True

