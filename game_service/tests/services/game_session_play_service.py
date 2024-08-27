import pytest
from unittest.mock import patch, MagicMock
from app.services.game_session_service import GameSessionService, DebitBalanceFromUserError, CreditBalanceToSlotMachineError, SlotMachineSpinError
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
def mock_slot_machine_by_id_service():
    with patch('app.services.game_session_service.SlotMachineByIdService') as mock_service:
        yield mock_service


@pytest.fixture
def game_session_service(mock_user_token_service, mock_slot_machine_service):
    mock_db = MagicMock()
    return GameSessionService(user_id="test_user", db=mock_db)


def test_play_game_debit_balance_error(game_session_service, mock_user_token_service, mock_slot_machine_service, mock_slot_machine_by_id_service):
    # Mock methods
    slot_machine_id = "machine_1"
    mock_user_token_service.return_value.debit_balance.return_value = False

    with pytest.raises(DebitBalanceFromUserError):
        game_session_service.play_game(slot_machine_id=slot_machine_id)


def test_play_game_credit_balance_to_machine_error(game_session_service, mock_user_token_service, mock_slot_machine_service, mock_slot_machine_by_id_service):
    # Mock methods
    slot_machine_id = "machine_1"
    mock_user_token_service.return_value.debit_balance.return_value = True
    mock_slot_machine_by_id_service.return_value.credit.return_value = False

    with pytest.raises(CreditBalanceToSlotMachineError):
        game_session_service.play_game(slot_machine_id=slot_machine_id)

    mock_user_token_service.return_value.debit_balance.assert_called_once()
    mock_slot_machine_by_id_service.return_value.credit.assert_called_once()


def test_prepare_session_spin_machine_error(game_session_service, mock_user_token_service, mock_slot_machine_service, mock_slot_machine_by_id_service):
    # Mock methods
    slot_machine_id = "machine_1"
    mock_user_token_service.return_value.debit_balance.return_value = True
    mock_slot_machine_by_id_service.return_value.credit.return_value = True
    mock_slot_machine_service.return_value.spin_machine.return_value = None

    with pytest.raises(SlotMachineSpinError):
        game_session_service.play_game(slot_machine_id=slot_machine_id)

    mock_user_token_service.return_value.debit_balance.assert_called_once()
    mock_slot_machine_by_id_service.return_value.credit.assert_called_once()
    mock_slot_machine_service.return_value.spin_machine.assert_called_once()
