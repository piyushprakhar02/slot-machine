import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.services.signup_service import UserSignupService, SignupUsernameExistsException, SignupVerificationException, SignupServiceException
from constant import Constant

client = TestClient(app)


@pytest.fixture
def mock_signup_service():
    with patch.object(UserSignupService, 'register') as mock_register:
        yield mock_register


@pytest.fixture
def mock_verify_service():
    with patch.object(UserSignupService, 'verify') as mock_verify:
        yield mock_verify


def test_signup_success(mock_signup_service):
    mock_signup_service.return_value = True
    data = {
        "email": "test@example.com",
        "password": "password123",
        "name": "testuser",
        "birthdate": "1990-01-01"
    }

    response = client.post("/signup", json=data)

    assert response.status_code == 200
    assert response.json() == {"success": True, "email": "test@example.com"}
    mock_signup_service.assert_called_once_with(data)


def test_signup_failure(mock_signup_service):
    mock_signup_service.side_effect = SignupUsernameExistsException()
    data = {
        "email": "test@example.com",
        "password": "password123",
        "name": "testuser",
        "birthdate": "1990-01-01"
    }

    response = client.post("/signup", json=data)

    assert response.status_code == 400
    assert response.json() == {"detail": Constant.SIGNUP_USER_EXISTS_EXCEPTION_MESSAGE}
    mock_signup_service.assert_called_once_with(data)


def test_verify_success(mock_verify_service):
    mock_verify_service.return_value = True
    data = {
        "email": "test@example.com",
        "totp": "123456"
    }

    response = client.post("/signup/verify", json=data)

    assert response.status_code == 200
    assert response.json() == {"success": True, "email": "test@example.com"}
    mock_verify_service.assert_called_once_with(data)


def test_verify_failure(mock_verify_service):
    mock_verify_service.side_effect = Exception()
    data = {
        "email": "test@example.com",
        "totp": "123456"
    }

    response = client.post("/signup/verify", json=data)

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}
    mock_verify_service.assert_called_once_with(data)
