import pytest
import os
from api import PetFriends
from settings import *

@pytest.fixture(scope="session")
def pf():
    """Initialize PetFriends API instance once per test session."""
    return PetFriends()

@pytest.fixture
def auth_key(pf):
    """Fetch a valid authentication key."""
    status, result = pf.get_api_key(valid_email, valid_password)
    assert status == 200, "Failed to get API key"
    assert "key" in result, "API key missing in response"
    return result["key"]

@pytest.fixture
def invalid_auth_key():
    """Return an invalid API key for negative test cases."""
    return "invalid_key_123"

@pytest.fixture
def pet_photo():
    """Return the full path to a valid pet photo."""
    return os.path.join(os.path.dirname(__file__), "images/cat1.jpg")