import pytest
from unittest.mock import patch, MagicMock
from app.services.game_session_service import GameSessionService, InsufficientTokensError, NoAvailableMachineError
from app.models import SlotMachine


@pytest.fixture
def mock_user_token_service():
    with patch('app.services.game_session_service.UserTokenService') as mock_service:
        yield mock_service


@pytest.fixture
def mock_slot_machine_service():
    with patch('app.services.game_session_service.SlotMachineService') as mock_service:
        yield mock_service


@pytest.fixture
def game_session_service(mock_user_token_service, mock_slot_machine_service):
    mock_db = MagicMock()
    return GameSessionService(user_id="test_user", db=mock_db)


def test_prepare_session_success(game_session_service, mock_user_token_service, mock_slot_machine_service):
    # Mock methods
    mock_user_token_service.return_value.get_balance.return_value = 5
    mock_slot_machine_service.return_value.allocate_machine.return_value = SlotMachine(id="machine_1")

    allocated_machine_id = game_session_service.prepare_session()

    assert allocated_machine_id == "machine_1"
    mock_user_token_service.return_value.get_balance.assert_called_once()
    mock_slot_machine_service.return_value.allocate_machine.assert_called_once()


def test_prepare_session_not_enough_tokens(game_session_service, mock_user_token_service, mock_slot_machine_service):
    # Mock methods
    mock_user_token_service.return_value.get_balance.return_value = 0
    mock_slot_machine_service.return_value.allocate_machine.return_value = SlotMachine(id="machine_1")

    # raises Exception
    with pytest.raises(InsufficientTokensError):
        game_session_service.prepare_session()

    mock_user_token_service.return_value.get_balance.assert_called_once()
    mock_slot_machine_service.return_value.allocate_machine.assert_called_once()


def test_prepare_session_no_available_machine(game_session_service, mock_user_token_service, mock_slot_machine_service):
    # Mock methods
    mock_user_token_service.return_value.get_balance.return_value = 5
    mock_slot_machine_service.return_value.allocate_machine.return_value = None

    # raises Exception
    with pytest.raises(NoAvailableMachineError):
        game_session_service.prepare_session()

    mock_user_token_service.return_value.get_balance.assert_called_once()
    mock_slot_machine_service.return_value.allocate_machine.assert_called_once()
