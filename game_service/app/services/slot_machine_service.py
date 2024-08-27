import random
from app.repositories.slot_machine_repository import SlotMachineRepository
from app.database import Session
from app.models import SlotMachine
from constant import Constant


class SlotMachineService:
    def __init__(self, db: Session):
        self.repository = SlotMachineRepository(db)

    def allocate_machine(self) -> SlotMachine:
        slot_machines = self.repository.get_available_machines()
        if not slot_machines:
            return None

        # Randomly pick a machine
        slot_machine = random.choice(slot_machines)

        # Set the machine status as busy
        self.repository.update_machine_status(slot_machine.id, Constant.SLOT_MACHINE_STATUS_BUSY)

        # Fetch the updated slot machine to return
        return self.repository.get_machine_by_id(slot_machine.id)

    def spin_machine(self) -> list:
        symbols = ['cherry', 'lemon', 'orange', 'bell', 'bar']
        result = [random.choice(symbols) for _ in range(4)]
        return result


class SlotMachineByIdService:
    def __init__(self, slot_machine_id: str, db: Session):
        self.slot_machine_id = slot_machine_id
        self.repository = SlotMachineRepository(db)

    def credit(self, count: int) -> bool:
        slot_machine = self.repository.get_machine_by_id(self.slot_machine_id)
        if slot_machine:
            self.repository.update_machine_balance(self.slot_machine_id, slot_machine.balance + count)
            return True

    def debit(self, count: int) -> bool:
        slot_machine = self.repository.get_machine_by_id(self.slot_machine_id)
        if slot_machine:
            self.repository.update_machine_balance(self.slot_machine_id, slot_machine.balance - count)
            return True

    def reset(self) -> None:
        self.repository.update_machine_balance(self.slot_machine_id, 0)
        return True

    def balance(self) -> int:
        slot_machine = self.repository.get_machine_by_id(self.slot_machine_id)
        return slot_machine.balance if slot_machine else 0
