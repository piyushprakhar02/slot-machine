import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.services.login_service import UserLoginService, LoginServiceException, InvalidCredentialsException
from constant import Constant

client = TestClient(app)


@pytest.fixture
def mock_login_service():
    with patch.object(UserLoginService, 'login') as mock_login:
        yield mock_login


def test_login_invalid_fields(mock_login_service):
    mock_login_service.return_value = "fake-jwt-token"
    response = client.post("/login", json={"invalidfield": "test@example.com", "password": "testpassword"})

    assert response.status_code == 422


def test_login_invalid_email(mock_login_service):
    mock_login_service.return_value = "fake-jwt-token"
    response = client.post("/login", json={"invalidfield": "testuser", "password": "testpassword"})

    assert response.status_code == 422


def test_successful_login(mock_login_service):
    mock_login_service.return_value = "fake-jwt-token"
    response = client.post("/login", json={"email": "test@example.com", "password": "testpassword"})

    assert response.status_code == 200
    assert response.json() == {"success": True, "token": "fake-jwt-token"}


def test_login_wrong_password(mock_login_service):
    mock_login_service.side_effect = InvalidCredentialsException()
    response = client.post("/login", json={"email": "test@example.com", "password": "wrongpassword"})

    assert response.status_code == 400
    assert response.json() == {"detail": Constant.LOGIN_INVALID_CREDENTIALS_ERROR_MESSAGE}


def test_login_service_exception(mock_login_service):
    mock_login_service.side_effect = LoginServiceException()
    response = client.post("/login", json={"email": "test@example.com", "password": "testpassword"})

    assert response.status_code == 400
    assert response.json() == {"detail": Constant.LOGIN_UNEXPECTED_ERROR_MESSAGE}


def test_internal_server_error(mock_login_service):
    mock_login_service.side_effect = Exception()
    response = client.post("/login", json={"email": "test@example.com", "password": "testpassword"})

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}
