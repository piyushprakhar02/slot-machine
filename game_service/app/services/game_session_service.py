from app.models import SlotMachine
from app.services.slot_token_service import UserTokenService
from app.services.slot_machine_service import SlotMachineService, SlotMachineByIdService
from constant import Constant
from app.database import Session


class GameSessionService:
    def __init__(self, user_id: str, db: Session):
        self.user_id = user_id
        self.slot_machine_service = SlotMachineService(db)
        self.db = db

    def prepare_session(self) -> SlotMachine:
        # Check if the user has enough tokens
        user_token_service = UserTokenService(user_id=self.user_id, db=self.db)
        balance = user_token_service.get_balance()

        if balance < 1:
            raise InsufficientTokensError()

        # Allocate a slot machine for the session
        slot_machine = self.slot_machine_service.allocate_machine()
        if slot_machine is None:
            raise NoAvailableMachineError()

        return slot_machine.id

    def play_game(self, slot_machine_id: str) -> int:
        # Check if the user has enough tokens
        user_token_service = UserTokenService(user_id=self.user_id, db=self.db)
        balance = user_token_service.get_balance()

        if balance < 1:
            raise InsufficientTokensError()

        # Debit token from user
        user_token_service = UserTokenService(user_id=self.user_id, db=self.db)
        debited = user_token_service.debit_balance(amount=Constant.TOKEN_NEEDED_PER_GAME)
        if debited is False:
            raise DebitBalanceFromUserError()

        # Credit token to slot machine
        slot_machine_by_id = SlotMachineByIdService(slot_machine_id=slot_machine_id, db=self.db)
        credited_to_machine = slot_machine_by_id.credit(count=Constant.TOKEN_NEEDED_PER_GAME)
        if credited_to_machine is False:
            raise CreditBalanceToSlotMachineError()

        # Spin the Slot Machine
        slots = self.slot_machine_service.spin_machine()
        if slots is None:
            raise SlotMachineSpinError()

        if slots[0] == slots[1] == slots[2] == slots[3]:
            slot_machine_by_id = SlotMachineByIdService(slot_machine_id=slot_machine_id, db=self.db)
            slot_machine_by_id.balance()
            return slot_machine_by_id.balance(), slots

        else:
            return 0, slots


class InsufficientTokensError(Exception):
    def __init__(self, message=Constant.INSUFFICIENT_TOKEN_EXCEPTION_MESSAGE):
        self.message = message
        super().__init__(self.message)


class NoAvailableMachineError(Exception):
    def __init__(self, message=Constant.SLOT_MACHINE_UNAVAILABLE_EXCEPTION_MESSAGE):
        self.message = message
        super().__init__(self.message)


class DebitBalanceFromUserError(Exception):
    def __init__(self, message=Constant.DEBIT_USER_BALANCE_EXCEPTION_MESSAGE):
        self.message = message
        super().__init__(self.message)


class CreditBalanceToSlotMachineError(Exception):
    def __init__(self, message=Constant.CREDIT_SLOT_MACHINE_BALANCE_EXCEPTION_MESSAGE):
        self.message = message
        super().__init__(self.message)


class SlotMachineSpinError(Exception):
    def __init__(self, message=Constant.SLOT_MACHINE_SPIN_EXCEPTION_MESSAGE):
        self.message = message
        super().__init__(self.message)
