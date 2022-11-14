import pytest
from app import utils

def test_verify_password():
    
    #hash for word "pass"
    hashed_pass= "$2b$12$3vjRF4p3SIRF5TfpnoxkYuxJD2ACsXlGhWm4MO5N96pPuL.FlFDd2"

    assert utils.verify_password('pass',hashed_pass) == True

