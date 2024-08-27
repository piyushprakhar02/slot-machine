import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.services.game_session_service import GameSessionService, InsufficientTokensError, NoAvailableMachineError
from constant import Constant

client = TestClient(app)


@pytest.fixture
def mock_prepare_session():
    with patch.object(GameSessionService, 'prepare_session', return_value='mock_machine_id') as mock_method:
        yield mock_method


def test_start_session_success(mock_prepare_session):
    user_id = "test_user"

    response = client.post(f"/game/{user_id}/start-session")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "allocated_machine_id": "mock_machine_id",
        "message": "Successfully Allocated"
    }

    # Ensure the mock was called
    mock_prepare_session.assert_called_once()


def test_start_session_insufficient_tokens(mock_prepare_session):
    user_id = "test_user"

    # Modify the mock to raise an InsufficientTokensError when called
    mock_prepare_session.side_effect = InsufficientTokensError()

    response = client.post(f"/game/{user_id}/start-session")

    assert response.status_code == 400
    assert response.json() == {"detail": Constant.INSUFFICIENT_TOKEN_EXCEPTION_MESSAGE}

    # Ensure the mock was called
    mock_prepare_session.assert_called_once()


def test_start_session_no_machine_avaialble(mock_prepare_session):
    user_id = "test_user"

    # Modify the mock to raise an InsufficientTokensError when called
    mock_prepare_session.side_effect = NoAvailableMachineError()

    response = client.post(f"/game/{user_id}/start-session")

    assert response.status_code == 503
    assert response.json() == {"detail": Constant.SLOT_MACHINE_UNAVAILABLE_EXCEPTION_MESSAGE}

    # Ensure the mock was called
    mock_prepare_session.assert_called_once()


def test_start_session_unkown_exception(mock_prepare_session):
    user_id = "test_user"

    # Modify the mock to raise an InsufficientTokensError when called
    mock_prepare_session.side_effect = Exception("Unknown error occurred")

    response = client.post(f"/game/{user_id}/start-session")

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}

    # Ensure the mock was called
    mock_prepare_session.assert_called_once()
