import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.services.game_session_service import GameSessionService, DebitBalanceFromUserError, CreditBalanceToSlotMachineError, SlotMachineSpinError
from constant import Constant

client = TestClient(app)


@pytest.fixture
def mock_prepare_session():
    with patch.object(GameSessionService, 'play_game') as mock_method:
        yield mock_method


def test_play_session_success_with_win(mock_prepare_session):
    mock_prepare_session.return_value = (100, ['cherry', 'cherry', 'cherry', 'cherry'])
    user_id = "test_user"
    slot_machine_id = "machine_1"

    response = client.post(f"/game/{user_id}/machine/{slot_machine_id}/play")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "slots": ['cherry', 'cherry', 'cherry', 'cherry'],
        "message": "Yay! You won the Jackpot worth 100"
    }


def test_play_session_success_with_lose(mock_prepare_session):
    mock_prepare_session.return_value = (0, ['cherry', 'lemon', 'cherry', 'cherry'])
    user_id = "test_user"
    slot_machine_id = "machine_1"

    response = client.post(f"/game/{user_id}/machine/{slot_machine_id}/play")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "slots": ['cherry', 'lemon', 'cherry', 'cherry'],
        "message": "Better luck next time!"
    }


def test_play_session_user_debit_token_failure(mock_prepare_session):
    user_id = "test_user"
    slot_machine_id = "machine_1"

    mock_prepare_session.side_effect = DebitBalanceFromUserError()

    response = client.post(f"/game/{user_id}/machine/{slot_machine_id}/play")

    assert response.status_code == 400
    assert response.json() == {"detail": Constant.DEBIT_USER_BALANCE_EXCEPTION_MESSAGE}


def test_play_session_machine_credit_token_failure(mock_prepare_session):
    user_id = "test_user"
    slot_machine_id = "machine_1"

    mock_prepare_session.side_effect = CreditBalanceToSlotMachineError()

    response = client.post(f"/game/{user_id}/machine/{slot_machine_id}/play")

    assert response.status_code == 503
    assert response.json() == {"detail": Constant.CREDIT_SLOT_MACHINE_BALANCE_EXCEPTION_MESSAGE}


def test_play_session_macine_spin_failure(mock_prepare_session):
    user_id = "test_user"
    slot_machine_id = "machine_1"

    mock_prepare_session.side_effect = SlotMachineSpinError()

    response = client.post(f"/game/{user_id}/machine/{slot_machine_id}/play")

    assert response.status_code == 503
    assert response.json() == {"detail": Constant.SLOT_MACHINE_SPIN_EXCEPTION_MESSAGE}


def test_start_session_unkown_exception(mock_prepare_session):
    user_id = "test_user"
    slot_machine_id = "machine_1"

    mock_prepare_session.side_effect = Exception()

    response = client.post(f"/game/{user_id}/machine/{slot_machine_id}/play")

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}
