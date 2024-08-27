import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.services.mfa_service import MFAService
from constant import Constant

client = TestClient(app)


@pytest.fixture
def mock_mfa_service():
    with patch.object(MFAService, 'initiate_mfa_setup') as mock_initiate_mfa_setup:
        yield mock_initiate_mfa_setup


@pytest.fixture
def mock_complete_mfa_service():
    with patch.object(MFAService, 'complete_mfa_setup') as mock_complete_mfa_setup:
        yield mock_complete_mfa_setup


def test_setup_mfa_success(mock_mfa_service):
    mock_mfa_service.return_value = "fake-setup-code"

    fake_jwt_token = "Bearer fake-jwt-token"

    response = client.post("/mfa/initiate", headers={"Authorization": fake_jwt_token})

    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "MFA setup initiated. Please configure your authenticator app.", "code": "fake-setup-code"}


def test_complete_mfa_setup_success(mock_complete_mfa_service):
    mock_mfa_service.return_value = True

    fake_jwt_token = "Bearer fake-jwt-token"

    response = client.post("/mfa/complete", json={"code": "fake-setup-code"}, headers={"Authorization": fake_jwt_token})

    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "MFA setup completed successfully"}
